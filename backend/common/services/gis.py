import os
import shutil
import zipfile
import logging
from uuid import uuid4
from typing import Any, Dict, List, Optional, Tuple

import geopandas as gpd
from django.conf import settings
from geopandas import GeoDataFrame
from shapely import wkb
from shapely.ops import transform
from shapely.validation import explain_validity

from common.exceptions import GeoFrameValidationError

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------- #
# Geometry helpers
# --------------------------------------------------------------------------- #
def drop_zm(geom):
    """Return the geometry with only X and Y (Z and M are dropped)."""
    if geom is None:
        return geom
    return transform(lambda *coords: coords[:2], geom)


def get_geometry_type(gdf: GeoDataFrame) -> str:
    """
    Return the geometry type of a GeoDataFrame, lowercased.

    The type of the first row is used (a warning is logged if types are mixed).
    One of: point, multipoint, linestring, multilinestring, polygon, multipolygon.
    Raises GeoFrameValidationError for any other type.
    """
    geom_types = gdf.geom_type.unique()

    if len(geom_types) > 1:
        logger.warning("Mixed geometry types detected: %s", list(geom_types))

    geometry_type = geom_types[0].lower()

    supported_types = {
        "point",
        "multipoint",
        "linestring",
        "multilinestring",
        "polygon",
        "multipolygon",
    }
    if geometry_type not in supported_types:
        raise GeoFrameValidationError(f"Unsupported geometry type: {geometry_type}")
    return geometry_type


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #
def validate_geodataframe(
    gdf: GeoDataFrame, validation_check: bool = False
) -> Tuple[bool, str]:
    """
    Validate a GeoDataFrame before processing.

    Args:
        gdf: GeoDataFrame with the shapefile data
        validation_check: also check that every geometry is topologically valid

    Returns:
        (is_valid, error_message)
    """
    if gdf.empty:
        return False, "GeoDataFrame contains no features"

    if validation_check:
        invalid_geoms = gdf[~gdf.geometry.is_valid]
        for idx, geom in invalid_geoms.geometry.items():
            logger.warning("Feature ID %s: %s", idx, explain_validity(geom))
        if not invalid_geoms.empty:
            return False, f"GeoDataFrame contains {len(invalid_geoms)} invalid geometries"

    if gdf.geometry.apply(lambda geom: geom.has_z if geom is not None else False).any():
        return False, "GeoDataFrame contains 3D geometries (Z values), which are not supported"

    return True, ""


# --------------------------------------------------------------------------- #
# Export
# --------------------------------------------------------------------------- #
def queryset_to_shapefile(
    queryset,
    geometry_field: str = "border",
    output_dir: Optional[str] = None,
    zip_output: bool = True,
    filename: Optional[str] = None,
    crs: str = "EPSG:3857",
    exclude_fields: Optional[List[str]] = None,
) -> str:
    """
    Export a queryset to an ESRI shapefile and return the path of the result.

    - every concrete field except `geometry_field` and the excluded ones becomes
      an attribute column (foreign keys are exported as raw ids)
    - many-to-many fields are exported as their related objects' str() joined by " - "
    - files are written under <output_dir or MEDIA_ROOT>; with `zip_output=True`
      the returned path is the .zip file, otherwise the .shp file
    """
    if not queryset.exists():
        raise GeoFrameValidationError("Queryset is empty — cannot create shapefile.")

    model = queryset.model
    all_fields = [f.name for f in model._meta.get_fields()]

    if geometry_field not in all_fields:
        raise GeoFrameValidationError(
            f"Geometry field '{geometry_field}' not found on model "
            f"'{model.__name__}'. Available fields: {all_fields}"
        )

    excluded = {"oldid", "created_at", "updated_at", "shr_layer", "shr_layer_id"}
    excluded.update(exclude_fields or [])

    # attname gives the raw DB value (e.g. dtyp_id) instead of the related object
    attribute_fields: List[str] = [
        f.attname
        for f in model._meta.get_fields()
        if hasattr(f, "column")
        and f.name != geometry_field
        and f.name not in excluded
    ]

    # M2M fields have no column, so they are collected separately
    m2m_fields: List[str] = [
        f.name for f in model._meta.many_to_many if f.name not in excluded
    ]

    records: List[Dict[str, Any]] = []
    rows = queryset.only(geometry_field, *attribute_fields).prefetch_related(*m2m_fields)

    for obj in rows:
        geom_value = getattr(obj, geometry_field)
        if geom_value is None:
            continue

        # Django GIS geometry -> Shapely geometry
        try:
            shapely_geom = wkb.loads(bytes(geom_value.wkb))
        except Exception as exc:
            raise GeoFrameValidationError(
                f"Failed to convert geometry for object pk={obj.pk}: {exc}"
            )

        if shapely_geom.has_z:
            shapely_geom = drop_zm(shapely_geom)

        row: Dict[str, Any] = {"geometry": shapely_geom}

        for field in attribute_fields:
            value = getattr(obj, field, None)
            # shapefiles don't support complex python types
            if isinstance(value, (dict, list)):
                value = str(value)
            row[field] = value

        for field in m2m_fields:
            row[field] = " - ".join(str(item) for item in getattr(obj, field).all())

        records.append(row)

    if not records:
        raise GeoFrameValidationError("Queryset produced no rows with valid geometries.")

    gdf = gpd.GeoDataFrame(records, geometry="geometry", crs=crs)

    is_valid, error_message = validate_geodataframe(gdf)
    if not is_valid:
        raise GeoFrameValidationError(
            f"Generated GeoDataFrame failed validation: {error_message}"
        )

    base_name = filename or str(uuid4())
    work_dir = output_dir or settings.MEDIA_ROOT
    shp_dir = os.path.join(work_dir, "exportedshapefiles", base_name)
    os.makedirs(shp_dir, exist_ok=True)

    shp_path = os.path.join(shp_dir, f"{base_name}.shp")
    gdf.to_file(shp_path, driver="ESRI Shapefile")

    if not zip_output:
        return shp_path

    zip_path = os.path.join(work_dir, f"{base_name}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for part in os.listdir(shp_dir):
            zf.write(os.path.join(shp_dir, part), arcname=part)  # flat structure

    # the raw shapefile directory is no longer needed once the zip is ready
    shutil.rmtree(shp_dir, ignore_errors=True)

    return zip_path