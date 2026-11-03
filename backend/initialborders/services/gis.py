import zipfile
import tempfile
import os
import shutil
from typing import Tuple, Dict, Any, Optional
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import geopandas as gpd
from geopandas import GeoDataFrame
from django.contrib.gis.geos import MultiPolygon, Polygon
from shapely.geometry import MultiPolygon as ShapelyMultiPolygon, Polygon as ShapelyPolygon

from django.core.files.uploadedfile import InMemoryUploadedFile

from common.services.gis_services import (
    validate_geodataframe , 
    get_geometry_type,
    drop_zm
)

def convert_gdf_to_multipolygon(gdf: GeoDataFrame) -> MultiPolygon:
    """
    Convert GeoDataFrame polygons to Django MultiPolygon
    
    Args:
        gdf: GeoDataFrame containing polygon geometries
        
    Returns:
        MultiPolygon: Django MultiPolygon object ready for model field
    """
    polygons = []
    
    for geom in gdf.geometry:
        if geom is None:
            continue
            
        # Handle different geometry types
        if geom.geom_type == 'Polygon':
            # Convert shapely Polygon to Django Polygon
            exterior_coords = list(geom.exterior.coords)
            interior_coords = [list(interior.coords) for interior in geom.interiors]
            
            django_polygon = Polygon(exterior_coords, *interior_coords)
            polygons.append(django_polygon)
            
        elif geom.geom_type == 'MultiPolygon':
            # Extract individual polygons from MultiPolygon
            for poly in geom.geoms:
                exterior_coords = list(poly.exterior.coords)
                interior_coords = [list(interior.coords) for interior in poly.interiors]
                
                django_polygon = Polygon(exterior_coords, *interior_coords)
                polygons.append(django_polygon)
    
    if not polygons:
        raise ValueError("No valid polygon geometries found")
    
    # Create MultiPolygon from all polygons
    return MultiPolygon(*polygons)

def proccess_initialborder_zipfile(
    zipfile_obj: InMemoryUploadedFile
) -> Tuple[bool, MultiPolygon, str]:
    """
    Process a ZIP file containing shapefile data for initial border
    
    Args:
        zipfile_obj: Uploaded ZIP file containing shapefile components
        
    Returns:
        tuple: (success: bool, multipolygon: MultiPolygon, error_message: str)
               On success: (True, MultiPolygon object, "")
               On failure: (False, None, error_message)
    """
    temp_dir = None
    
    try:
        # Reset file pointer to beginning
        zipfile_obj.seek(0)
        
        # Create temporary directory for extraction
        temp_dir = tempfile.mkdtemp()
        
        # Extract ZIP file contents
        with zipfile.ZipFile(zipfile_obj, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find shapefile (.shp file)
        shp_file = None
        extracted_files = os.listdir(temp_dir)
        
        for file in extracted_files:
            if file.lower().endswith('.shp'):
                shp_file = os.path.join(temp_dir, file)
                break
        
        if not shp_file:
            return False, None, 'فایلی با فرمت .shp در زیپ فایل یافت نشد'
        
        # Check for required shapefile components
        base_name = os.path.splitext(shp_file)[0]
        required_extensions = ['.shp', '.shx', '.dbf']
        missing_files = []
        
        for ext in required_extensions:
            if not os.path.exists(base_name + ext):
                missing_files.append(ext)
        
        if missing_files:
            return False, None, f'این فایل ها در زیپ فایل یافت نشد: {missing_files}'
        
        # Read shapefile into GeoDataFrame
        try:
            gdf = gpd.read_file(shp_file)
        except Exception as e:
            return False, None, f'خطا در خواندن شیپ فایل: {str(e)}'
        
        # Drop Zm
        try:
            gdf.geometry = gdf.geometry.apply(drop_zm)
        except Exception as e:
            return False, None, f'خطا در حذف zm از فایل'
        
        # Validate GeoDataFrame
        is_valid, validation_error = validate_geodataframe(gdf , validation_check=True)
        if not is_valid:
            return False, None, f'خطا در شیپ فایل ورودی: {validation_error}'
        
        # Get geometry type
        try:
            geometry_type = get_geometry_type(gdf)
        except Exception as e:
            return False, None, f'نوع هندسی شیپ فایل ورودی تشخص داده نشد: {str(e)}'
        
        # Check if geometry type is polygon (required for MultiPolygonField)
        # the multipolygon is allowed to database but (as a one row !)
        #if geometry_type != 'polygon':
        #    return False, None, f'نوع هندسی شیپ فایل باید polygon یا multipolygon باشد: {geometry_type}'
        
        # Check CRS and reproject if needed
        if gdf.crs is None:
            return False, None, 'مختصات شیپ ورودی صحیح نمی‌باشد'
        
        # Convert to WGS84 (EPSG:4326) if not already
        if gdf.crs.to_epsg() != 4326:
            try:
                gdf = gdf.to_crs(epsg=4326)
            except Exception as e:
                return False, None, f'خطا در مختصات شیپ فایل: {str(e)}'
        
        # Convert geometries to Django MultiPolygon
        try:
            multipolygon = convert_gdf_to_multipolygon(gdf)
        except Exception as e:
            return False, None, f'خطا در ساخت multipolygon: {str(e)}'
        
        # Return successful result
        return True, multipolygon, ""
        
    except zipfile.BadZipFile:
        return False, None, 'زیپ فایل نامعتبر می‌باشد'
    except Exception as e:
        return False, None, f'Unexpected error processing ZIP file: {str(e)}'
    
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Warning: Failed to clean up temporary directory: {e}")