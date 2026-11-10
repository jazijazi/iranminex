import os
import tempfile
import zipfile
from typing import Optional, Tuple

import geopandas as gpd
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.files.uploadedfile import UploadedFile
from geopandas import GeoDataFrame

from common.services.gis import drop_zm, validate_geodataframe


def convert_gdf_to_multipolygon(gdf: GeoDataFrame) -> MultiPolygon:
    """
    Merge every Polygon / MultiPolygon row of a GeoDataFrame (EPSG:3857)
    into one Django MultiPolygon. Other geometry types and empty rows are skipped.
    """
    polygons = []

    for geom in gdf.geometry:
        if geom is None:
            continue

        if geom.geom_type == "Polygon":
            shapely_polygons = [geom]
        elif geom.geom_type == "MultiPolygon":
            shapely_polygons = list(geom.geoms)
        else:
            continue

        for poly in shapely_polygons:
            exterior = list(poly.exterior.coords)
            interiors = [list(interior.coords) for interior in poly.interiors]
            polygons.append(Polygon(exterior, *interiors))

    if not polygons:
        raise ValueError("No valid polygon geometries found")

    return MultiPolygon(*polygons, srid=3857)


def proccess_initialborder_zipfile(
    zipfile_obj: UploadedFile,
) -> Tuple[bool, Optional[MultiPolygon], str]:
    """
    Read a zipped shapefile and convert it to one Django MultiPolygon (EPSG:3857).

    Returns:
        (True, MultiPolygon, "")         on success
        (False, None, error_message)     on failure
    """
    try:
        zipfile_obj.seek(0)

        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zipfile_obj, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            # lowercase name -> real name, so extensions are matched case-insensitively
            files = {name.lower(): name for name in os.listdir(temp_dir)}

            shp_key = next((name for name in sorted(files) if name.endswith(".shp")), None)
            if shp_key is None:
                return False, None, "فایلی با فرمت .shp در زیپ فایل یافت نشد"

            base_name = os.path.splitext(shp_key)[0]
            missing_files = [
                ext for ext in (".shp", ".shx", ".dbf") if base_name + ext not in files
            ]
            if missing_files:
                return False, None, f"این فایل ها در زیپ فایل یافت نشد: {missing_files}"

            try:
                gdf = gpd.read_file(os.path.join(temp_dir, files[shp_key]))
            except Exception as e:
                return False, None, f"خطا در خواندن شیپ فایل: {str(e)}"

            try:
                gdf.geometry = gdf.geometry.apply(drop_zm)
            except Exception:
                return False, None, "خطا در حذف zm از فایل"

            is_valid, validation_error = validate_geodataframe(gdf, validation_check=True)
            if not is_valid:
                return False, None, f"خطا در شیپ فایل ورودی: {validation_error}"

            if gdf.crs is None:
                return False, None, "مختصات شیپ ورودی صحیح نمی‌باشد"

            if gdf.crs.to_epsg() != 3857:
                try:
                    gdf = gdf.to_crs(epsg=3857)
                except Exception as e:
                    return False, None, f"خطا در مختصات شیپ فایل: {str(e)}"

            try:
                multipolygon = convert_gdf_to_multipolygon(gdf)
            except Exception as e:
                return False, None, f"خطا در ساخت multipolygon: {str(e)}"

            return True, multipolygon, ""

    except zipfile.BadZipFile:
        return False, None, "زیپ فایل نامعتبر می‌باشد"
    except Exception as e:
        return False, None, f"Unexpected error processing ZIP file: {str(e)}"