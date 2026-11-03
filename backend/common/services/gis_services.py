import os
import zipfile
import shutil
from urllib.parse import quote_plus
from uuid import uuid4
from typing import List , Tuple , Dict , Any , TypedDict
from django.core.files.uploadedfile import InMemoryUploadedFile

from common.exceptions import (
    GeoFrameValidationError,
)

import fiona
import geopandas as gpd
from geopandas import GeoDataFrame
from django.conf import settings
from shapely.geometry import MultiPolygon, Polygon

from shapely.ops import transform
from shapely.validation import explain_validity

# from layercore.services.tablename_service import add_unique_suffix_to_tablename

# from layercore.utils import (
#     GeoFrameValidationError,
#     GeoServerError,
#     ShapefileValidationError,
#     SldValidationError,
#     GeoDatabaseValidationError,
# )

def drop_zm(geom):
    return transform(lambda *coords: coords[:2], geom)

def validate_geodataframe(gdf : GeoDataFrame , validation_check : bool = False) -> Tuple[bool, str]:
    """
    Validate the GeoDataFrame data before processing
    
    Args:
        gdf: GeoDataFrame with the shapefile data
        validation_check: a boolean flag to choose check geometry or not 
        
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if geodataframe is empty
    if gdf.empty:
        return False, "GeoDataFrame contains no features"
    
    # Check for valid geometries
    if validation_check:
        invalid_geoms = gdf[~gdf.geometry.is_valid]
        for idx, geom in invalid_geoms.geometry.items():
            print(f"Feature ID {idx}: {explain_validity(geom)}")
        if not invalid_geoms.empty:
            return False, f"GeoDataFrame contains {len(invalid_geoms)} invalid geometries"
    
    # Check for Z dimension
    if gdf.geometry.apply(lambda geom: geom.has_z if geom is not None else False).any():
        return False, "GeoDataFrame contains 3D geometries (Z values), which are not supported"
        
    return True, ""

def get_geometry_type(gdf:GeoDataFrame) -> str:
    """
    Determine the geometry type from a GeoDataFrame
    
    Args:
        gdf: GeoDataFrame with the shapefile data
        
    Returns:
        str: One of 'point', 'line', 'polygon' or raises error
    """
    # Get unique geometry types (there might be multiple)
    geom_types = gdf.geom_type.unique()
    
    # Check for mixed geometry types
    if len(geom_types) > 1:
        print(f"Mixed geometry types detected: {geom_types}")
    
    # Use the first/predominant type for classification
    geometry_type = geom_types[0].lower()
    
    geometry_mapping = {
        'point': 'point',
        'multipoint': 'multipoint',
        'linestring': 'linestring',
        'multilinestring': 'multilinestring',
        'polygon': 'polygon',
        'multipolygon': 'multipolygon'
    }
    
    if geometry_type in geometry_mapping:
        return geometry_mapping[geometry_type]
    else:
        raise GeoFrameValidationError(f"Unsupported geometry type: {geometry_type}")
    

def queryset_to_shapefile(
    queryset,
    geometry_field: str = "border",
    output_dir: str = None,
    zip_output: bool = True,
    filename: str = None,
    crs: str = "EPSG:4326",
    exclude_fields: List[str] = None,
) -> str:

    DEFAULT_EXCLUDED_FIELDS: set = {"oldid", "created_at", "updated_at","shr_layer","shr_layer_id"}

    if not queryset.exists():
        raise GeoFrameValidationError("Queryset is empty — cannot create shapefile.")

    model = queryset.model
    all_fields = [f.name for f in model._meta.get_fields()]

    if geometry_field not in all_fields:
        raise GeoFrameValidationError(
            f"Geometry field '{geometry_field}' not found on model "
            f"'{model.__name__}'. Available fields: {all_fields}"
        )

    # Merge default excluded fields with any caller-supplied extras
    excluded: set = DEFAULT_EXCLUDED_FIELDS.copy()

    if exclude_fields:
        excluded.update(exclude_fields)

    # Collect every non-geometry, concrete, non-excluded field
    attribute_fields: List[str] = [
        f.attname  # ← attname gives raw DB value (e.g. dtyp_id) instead of f.name (e.g. dtyp) which triggers __str__
        for f in model._meta.get_fields()
        if hasattr(f, "column")
        and f.name != geometry_field
        and f.name not in excluded
    ]

    # Collect M2M fields (they have no column so were excluded above)
    m2m_fields: List[str] = [
        f.name
        for f in model._meta.many_to_many
        if f.name not in excluded
    ]

    from shapely import wkb  # lazy import — already a geopandas dependency

    records: List[Dict[str, Any]] = []

    for obj in queryset.only(geometry_field, *attribute_fields):
        geom_value = getattr(obj, geometry_field)
        if geom_value is None:
            continue  # skip null-geometry rows

        # Django GIS geometry → Shapely geometry via WKB
        try:
            shapely_geom = wkb.loads(bytes(geom_value.wkb))
        except Exception as exc:
            raise GeoFrameValidationError(
                f"Failed to convert geometry for object pk={obj.pk}: {exc}"
            )

        # Drop Z/M dimensions if present
        if shapely_geom.has_z:
            shapely_geom = drop_zm(shapely_geom)

        row: Dict[str, Any] = {"geometry": shapely_geom}
        for field in attribute_fields:
            value = getattr(obj, field, None)
            # Shapefiles don't support complex Python types
            if isinstance(value, (dict, list)):
                value = str(value)
            row[field] = value

        # M2M fields — join all related __str__ values with ' - '
        for field in m2m_fields:
            related_qs = getattr(obj, field).all()
            row[field] = " - ".join(str(item) for item in related_qs)


        records.append(row)

    if not records:
        raise GeoFrameValidationError(
            "Queryset produced no rows with valid geometries."
        )

    gdf = gpd.GeoDataFrame(records, geometry="geometry", crs=crs)

    is_valid, error_message = validate_geodataframe(gdf)
    if not is_valid:
        raise GeoFrameValidationError(
            f"Generated GeoDataFrame failed validation: {error_message}"
        )

    base_name = filename or str(uuid4())
    # work_dir = output_dir or tempfile.mkdtemp()
    work_dir = settings.MEDIA_ROOT
    shp_dir = os.path.join(work_dir,'exportedshapefiles' , base_name)
    os.makedirs(shp_dir, exist_ok=True)

    shp_path = os.path.join(shp_dir, f"{base_name}.shp")
    gdf.to_file(shp_path, driver="ESRI Shapefile")

    if not zip_output:
        return shp_path

    zip_path = os.path.join(work_dir, f"{base_name}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for part in os.listdir(shp_dir):
            zf.write(
                os.path.join(shp_dir, part),
                arcname=part,   # flat structure inside the zip
            )

    # Clean up the raw shapefile directory now that the zip is ready
    shutil.rmtree(shp_dir, ignore_errors=True)


    return zip_path