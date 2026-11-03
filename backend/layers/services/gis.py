import zipfile
import uuid
import tempfile
import os
import json
import shutil
import subprocess
from typing import Tuple, Dict, Any, Optional, List
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import geopandas as gpd
import fiona
from geopandas import GeoDataFrame
from django.contrib.gis.geos import MultiPolygon, Polygon, Point, LineString, MultiPoint, MultiLineString
from django.contrib.gis import geos
from shapely.geometry import (
    MultiPolygon as ShapelyMultiPolygon, 
    Polygon as ShapelyPolygon, 
    Point as ShapelyPoint,
    LineString as ShapelyLineString,
    MultiPoint as ShapelyMultiPoint,
    MultiLineString as ShapelyMultiLineString
)
from django.contrib.gis.db import models as gis_models
from django.conf import settings
import pandas as pd
from datetime import datetime

from layers.exceptions import (
    GeoDatabaseValidationError,
)

from common.services.gis_services import (
    validate_geodataframe,
    get_geometry_type,
    drop_zm,
)

def get_shape_columns_from_zipfile(
    zipfile_obj: InMemoryUploadedFile,
        
) -> Tuple[bool, Optional[List[str]], str]:
    """
    validate the zipeed shapefile and 
    if valid return columns of shpefile as 
    
    Args:
        zipfile_obj: Uploaded zip file containing shapefile
        
    Returns:
        tuple: (success, processed_data, message)
            - success: Boolean indicating if processing was successful
            - processed_data: List of dictionaries with processed feature data (None if error)
            - message: Error or success message

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
            return False, None, f'این فایل‌ها در زیپ فایل یافت نشد: {missing_files}'
        
        # Read shapefile into GeoDataFrame
        try:
            gdf = gpd.read_file(shp_file)
        except Exception as e:
            return False, None, f'خطا در خواندن شیپ فایل: {str(e)}'
        
        # Drop Zm
        try:
            gdf.geometry = gdf.geometry.apply(drop_zm)
        except Exception as e:
            print(">>>>>>>>>>>" , e)
            return False, None, f'خطا در حذف zm از فایل'
        
        # Validate GeoDataFrame using common service
        is_valid, validation_error = validate_geodataframe(gdf , validation_check=False)
        if not is_valid:
            return False, None, f'خطا در اعتبارسنجی شیپ فایل: {validation_error}'
        
        # Check if GeoDataFrame has columns
        if gdf.columns.empty:
            return False, None, "شیپ فایل هیچ ستونی ندارد"
        
        # Get geometry type from shapefile
        try:
            shapefile_geometry_type = get_geometry_type(gdf)
        except Exception as e:
            return False, None, f'خطا در تشخیص نوع هندسه: {str(e)}'
    
        return True , gdf.columns.tolist() , "گرفتن نام ستون های شیپ فایل با موفقیت انجام شد"
    
    except zipfile.BadZipFile:
        return False, None, "فایل zip معتبر نیست"
    except Exception as e:
        print(e)
        return False, None, f"خطا در پردازش فایل: {str(e)}"
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass  # Ignore cleanup errors

def process_layer_data(
    zipfile_obj: InMemoryUploadedFile,
    layer_model: Any,
    matched_fields: Dict[str, str],
    shrh_layer_instance: Any
) -> Tuple[bool, Optional[List[Dict[str, Any]]], str]:
    """
    Process uploaded zipfile containing shapefile data for layer border
    
    Args:
        zipfile_obj: Uploaded zip file containing shapefile
        layer_model: Django model class for the layer
        matched_fields: Dict mapping database field names to shapefile column names
        shrh_layer_instance: ShrhLayer instance
        
    Returns:
        tuple: (success, processed_data, message)
            - success: Boolean indicating if processing was successful
            - processed_data: List of dictionaries with processed feature data (None if error)
            - message: Error or success message
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
            return False, None, f'این فایل‌ها در زیپ فایل یافت نشد: {missing_files}'
        
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
        
        # Validate GeoDataFrame using common service
        is_valid, validation_error = validate_geodataframe(gdf , validation_check=False)
        if not is_valid:
            return False, None, f'خطا در اعتبارسنجی شیپ فایل: {validation_error}'
        
        # Get geometry type from shapefile
        try:
            shapefile_geometry_type = get_geometry_type(gdf)
        except Exception as e:
            return False, None, f'خطا در تشخیص نوع هندسه: {str(e)}'
        
        # Find geometry field in the model dynamically
        geometry_field = None
        geometry_field_name = None
        
        for field in layer_model._meta.get_fields():
            if isinstance(field, (gis_models.GeometryField, gis_models.PointField, 
                                gis_models.LineStringField, gis_models.PolygonField,
                                gis_models.MultiPointField, gis_models.MultiLineStringField,
                                gis_models.MultiPolygonField)):
                geometry_field = field
                geometry_field_name = field.name
                break
        
        if not geometry_field:
            return False, None, 'فیلد هندسه در مدل یافت نشد'
        
        # Check geometry compatibility
        model_geom_type = type(geometry_field).__name__
        compatibility = check_geometry_compatibility(shapefile_geometry_type, model_geom_type)
        
        if not compatibility['compatible']:
            return False, None, compatibility['error_message']
        
        # Convert CRS to EPSG:4326 if needed
        if gdf.crs is None:
            return False, None, "سیستم مختصات فایل شیپ مشخص نیست"
        
        if gdf.crs.to_epsg() != 4326:
            try:
                gdf = gdf.to_crs(epsg=4326)
            except Exception as e:
                return False, None, f"خطا در تبدیل سیستم مختصات: {str(e)}"
        
        # Process features
        processed_data = []
        
        for idx, row in gdf.iterrows():
            feature_data = {'shr_layer': shrh_layer_instance}
            geometry = row.geometry
            
            if geometry is None or geometry.is_empty:
                return False, None, f"هندسه خالی در ردیف {idx + 1} یافت شد"
            
            # Convert geometry to appropriate Django geometry type
            try:
                django_geom = convert_geometry_to_django(geometry, model_geom_type)
                feature_data[geometry_field_name] = django_geom
            except Exception as e:
                return False, None, f"خطا در تبدیل هندسه در ردیف {idx + 1}: {str(e)}"
            
            
            # Process non-geometry fields using matched_fields mapping
            
            # Normalize matched_fields: lowercase both keys and values
            normalized_matched_fields = {
                db_field.lower().strip(): shp_column.strip() 
                for db_field, shp_column in matched_fields.items()
            }
            # Normalize model field names once
            model_field_names = {
                f.name.lower(): f.name for f in layer_model._meta.get_fields()
            }
            # Normalize shapefile columns
            shapefile_columns = {col.lower(): col for col in gdf.columns}

            for db_field_lower, shp_column in normalized_matched_fields.items():
                if db_field_lower in model_field_names:
                    db_field = model_field_names[db_field_lower]
                else:
                    continue  # Skip unmatched fields

                shp_column_lower = shp_column.lower()
                if shp_column_lower not in shapefile_columns:
                    continue  # Skip if shapefile column not present

                original_column_name = shapefile_columns[shp_column_lower]
                value = row[original_column_name]                    
                # Handle null/nan values
                if pd.isna(value):
                    value = None
                
                # Get field type from model
                try:
                    model_field = layer_model._meta.get_field(db_field)
                    converted_value = convert_field_value(value, model_field)
                    feature_data[db_field] = converted_value
                except Exception as e:
                    return False, None, f"خطا در تبدیل فیلد {db_field}: {str(e)}"
                    
            print("---------------------")
            print(feature_data)
            print("---------------------")
            processed_data.append(feature_data)
        
        return True, processed_data, f"فایل با موفقیت پردازش شد. {len(processed_data)} ویژگی یافت شد"
        
    except zipfile.BadZipFile:
        return False, None, "فایل zip معتبر نیست"
    except Exception as e:
        print(e)
        return False, None, f"خطا در پردازش فایل: {str(e)}"
    
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass  # Ignore cleanup errors


def check_geometry_compatibility(shapefile_geom_type: str, model_geom_type: str) -> Dict[str, Any]:
    """
    Check if shapefile geometry type is compatible with model geometry field
    
    Args:
        shapefile_geom_type: Geometry type from shapefile (Point, Polygon, etc.)
        model_geom_type: Django geometry field type name
        
    Returns:
        dict: {'compatible': bool, 'error_message': str}
    """
    # Convert inputs to lowercase for case-insensitive comparison
    shapefile_geom_type_lower = shapefile_geom_type.lower()
    model_geom_type_lower = model_geom_type.lower()
    
    # Define compatibility matrix (all lowercase)
    #Key is model geom type and value is shape file geom that allowed for it
    compatibility_matrix = {
        'pointfield': ['point'],
        'multipointfield': ['point', 'multipoint'],
        'linestringfield': ['linestring'],
        'multilinestringfield': ['linestring', 'multilinestring'],
        'polygonfield': ['polygon'],
        'multipolygonfield': ['polygon', 'multipolygon'],
        'geometryfield': ['point', 'linestring', 'polygon', 'multipoint', 'multilinestring', 'multipolygon']
    }

    print(">>>>>>>>>>>>shapefile_geom_type_lower>>>>>>  " , shapefile_geom_type_lower)
    print(">>>>>>>>>>>>model_geom_type_lower>>>>>>  " , model_geom_type_lower)
    
    allowed_types = compatibility_matrix.get(model_geom_type_lower, [])
    
    if shapefile_geom_type_lower in allowed_types:
        return {'compatible': True, 'error_message': ''}
    else:
        return {
            'compatible': False, 
            'error_message': f'نوع هندسه {shapefile_geom_type} با فیلد {model_geom_type} سازگار نیست. انواع مجاز: {allowed_types}'
        }


def convert_geometry_to_django(shapely_geom, model_geom_type: str):
    """
    Convert Shapely geometry to appropriate Django geometry
    
    Args:
        shapely_geom: Shapely geometry object
        model_geom_type: Django geometry field type name
        
    Returns:
        Django geometry object
    """
    # Make case-insensitive
    model_geom_type_lower = model_geom_type.lower()
    
    if model_geom_type_lower == 'pointfield':
        if isinstance(shapely_geom, ShapelyPoint):
            return Point(shapely_geom.x, shapely_geom.y, srid=4326)
        else:
            raise ValueError(f"Cannot convert {type(shapely_geom).__name__} to Point")
    
    elif model_geom_type_lower == 'multipointfield':
        if isinstance(shapely_geom, ShapelyPoint):
            return MultiPoint([Point(shapely_geom.x, shapely_geom.y, srid=4326)])
        elif isinstance(shapely_geom, ShapelyMultiPoint):
            points = [Point(pt.x, pt.y, srid=4326) for pt in shapely_geom.geoms]
            return MultiPoint(points)
        else:
            raise ValueError(f"Cannot convert {type(shapely_geom).__name__} to MultiPoint")
    
    elif model_geom_type_lower == 'linestringfield':
        if isinstance(shapely_geom, ShapelyLineString):
            return LineString(list(shapely_geom.coords), srid=4326)
        else:
            raise ValueError(f"Cannot convert {type(shapely_geom).__name__} to LineString")
    
    elif model_geom_type_lower == 'multilinestringfield':
        if isinstance(shapely_geom, ShapelyLineString):
            # Convert single LineString to MultiLineString
            # Create a LineString object first, then wrap it in MultiLineString
            line_string = LineString(list(shapely_geom.coords), srid=4326)
            return MultiLineString([line_string], srid=4326)
        elif isinstance(shapely_geom, ShapelyMultiLineString):
            # Create individual LineString objects for each line
            line_strings = []
            for line in shapely_geom.geoms:
                line_string = LineString(list(line.coords), srid=4326)
                line_strings.append(line_string)
            return MultiLineString(line_strings, srid=4326)
        else:
            raise ValueError(f"Cannot convert {type(shapely_geom).__name__} to MultiLineString")
    
    elif model_geom_type_lower == 'polygonfield':
        if isinstance(shapely_geom, ShapelyPolygon):
            # Handle polygons with holes properly
            exterior_coords = list(shapely_geom.exterior.coords)
            interior_rings = [list(interior.coords) for interior in shapely_geom.interiors]
            return Polygon(exterior_coords, *interior_rings, srid=4326)
        else:
            raise ValueError(f"Cannot convert {type(shapely_geom).__name__} to Polygon")
    
    elif model_geom_type_lower == 'multipolygonfield':
        if isinstance(shapely_geom, ShapelyPolygon):
            # Handle polygons with holes properly
            exterior_coords = list(shapely_geom.exterior.coords)
            interior_rings = [list(interior.coords) for interior in shapely_geom.interiors]
            polygon = Polygon(exterior_coords, *interior_rings, srid=4326)
            return MultiPolygon([polygon], srid=4326)
        elif isinstance(shapely_geom, ShapelyMultiPolygon):
            polygons = []
            for poly in shapely_geom.geoms:
                exterior_coords = list(poly.exterior.coords)
                interior_rings = [list(interior.coords) for interior in poly.interiors]
                polygon = Polygon(exterior_coords, *interior_rings, srid=4326)
                polygons.append(polygon)
            return MultiPolygon(polygons, srid=4326)
        else:
            raise ValueError(f"Cannot convert {type(shapely_geom).__name__} to MultiPolygon")
    
    elif model_geom_type_lower == 'geometryfield':
        # GeometryField can accept any geometry type
        if isinstance(shapely_geom, ShapelyPoint):
            return Point(shapely_geom.x, shapely_geom.y, srid=4326)
        elif isinstance(shapely_geom, ShapelyLineString):
            return LineString(list(shapely_geom.coords), srid=4326)
        elif isinstance(shapely_geom, ShapelyPolygon):
            # Handle polygons with holes properly
            exterior_coords = list(shapely_geom.exterior.coords)
            interior_rings = [list(interior.coords) for interior in shapely_geom.interiors]
            return Polygon(exterior_coords, *interior_rings, srid=4326)
        elif isinstance(shapely_geom, ShapelyMultiPoint):
            points = [Point(pt.x, pt.y, srid=4326) for pt in shapely_geom.geoms]
            return MultiPoint(points)
        elif isinstance(shapely_geom, ShapelyMultiLineString):
            line_strings = []
            for line in shapely_geom.geoms:
                line_string = LineString(list(line.coords), srid=4326)
                line_strings.append(line_string)
            return MultiLineString(line_strings, srid=4326)
        elif isinstance(shapely_geom, ShapelyMultiPolygon):
            polygons = []
            for poly in shapely_geom.geoms:
                exterior_coords = list(poly.exterior.coords)
                interior_rings = [list(interior.coords) for interior in poly.interiors]
                polygon = Polygon(exterior_coords, *interior_rings, srid=4326)
                polygons.append(polygon)
            return MultiPolygon(polygons, srid=4326)
        else:
            raise ValueError(f"Unsupported geometry type: {type(shapely_geom).__name__}")
    
    else:
        raise ValueError(f"Unsupported model geometry type: {model_geom_type}")


def convert_field_value(value: Any, model_field) -> Any:
    """
    Convert shapefile field value to appropriate type for Django model field
    
    Args:
        value: Value from shapefile
        model_field: Django model field instance
        
    Returns:
        Converted value appropriate for the model field
    """
    if value is None or pd.isna(value):
        return None
    
    field_type = type(model_field).__name__
    
    try:
        if field_type in ['CharField', 'TextField']:
            return str(value).strip() if value else None
        
        elif field_type in ['IntegerField', 'PositiveIntegerField', 'BigIntegerField', 'PositiveBigIntegerField']:
            if isinstance(value, str) and value.strip() == '':
                return None
            return int(float(value))  # Handle cases where int comes as float
        
        elif field_type in ['FloatField', 'DecimalField']:
            if isinstance(value, str) and value.strip() == '':
                return None
            return float(value)
        
        elif field_type == 'BooleanField':
            if isinstance(value, str):
                return value.lower() in ['true', '1', 'yes', 'on', 'بله', 'درست']
            return bool(value)
        
        elif field_type in ['DateField', 'DateTimeField']:
            if isinstance(value, str) and value.strip():
                # Try different date formats
                date_formats = [
                    '%Y-%m-%d',
                    '%d/%m/%Y', 
                    '%m/%d/%Y',
                    '%Y/%m/%d',
                    '%d-%m-%Y',
                    '%m-%d-%Y'
                ]
                
                for fmt in date_formats:
                    try:
                        parsed_date = datetime.strptime(value.strip(), fmt)
                        if field_type == 'DateField':
                            return parsed_date.date()
                        else:
                            return parsed_date
                    except ValueError:
                        continue
                
                return None  # If no format matches
            elif hasattr(value, 'date'):
                return value.date() if field_type == 'DateField' else value
            else:
                return None
        
        else:
            # For other field types, return as string
            return str(value).strip() if value else None
            
    except (ValueError, TypeError, AttributeError):
        return None
    

def convert_tif_to_cog_and_save_to_rasterdir(tif_file:InMemoryUploadedFile) -> Tuple[bool, uuid.UUID , str]:
    """
        Converts a TIFF file to Cloud Optimized GeoTIFF (COG) using gdal_translate.
        Cloud Optimized GeoTIFF is useful for titiler

        Args:
            tif_fiel (str): A file with .tif extension

        Returns:
            tuple: (success, raster_uuid , message)
            - success: Boolean indicating if processing was successful
            - raster_uuid: a uuid of raster to store in database connected to /RASTERDIR/<Raster uuid>/output_cog.tif 
            - message: Error or success message
    """
    THIS_UUID = uuid.uuid4()

    temp_tiff_file_path = os.path.join(tempfile.gettempdir(), f"{THIS_UUID}.tif")

    try:

        # Save the file temporarily
        with open(temp_tiff_file_path, "wb+") as destination:
            for chunk in tif_file.chunks():
                destination.write(chunk)

        if not os.path.isfile(temp_tiff_file_path) or not temp_tiff_file_path.lower().endswith(".tif"):
            raise ValueError("Invalid TIFF file path provided.")
        
        main_raster_dir = settings.RASTER_ROOT

        current_raster_dir = os.path.join(main_raster_dir, str(THIS_UUID))
        os.makedirs(current_raster_dir, exist_ok=True)

        output_cog_path = os.path.join(current_raster_dir, "output_cog.tif")

        gdal_translate_path = shutil.which("gdal_translate")
        if not gdal_translate_path:
            raise RuntimeError("gdal_translate not found in PATH")
        
        try:
            # Convert to COG format with LZW compression and automatic overviews
            translate_cmd = [
                gdal_translate_path, "-of", "COG",
                "-co", "COMPRESS=LZW",
                "-co", "OVERVIEWS=AUTO",
                temp_tiff_file_path, output_cog_path
            ]
            subprocess.run(translate_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            return True , THIS_UUID , "لایه رستری با موفقیت بارگذاری شد"

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error while processing: {e.stderr.decode()}")

    except Exception as e:
        print(e)
        return False, None, f"خطا در پردازش فایل رستری: {str(e)}"
    
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_tiff_file_path):
            os.remove(temp_tiff_file_path)

def get_layersnames_from_zipped_geodatabase(
  gdb_zip_file:InMemoryUploadedFile,   
) -> List[str]:
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        zip_path = os.path.join(tmpdirname, f"gdbzipfile_{uuid.uuid4().hex[:8]}.zip")

        # Save the uploaded file to the temp directory
        with open(zip_path, 'wb+') as f:
            for chunk in gdb_zip_file.chunks():
                f.write(chunk)
        
        try:
            # Extract zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)
        except zipfile.BadZipFile:
            raise GeoDatabaseValidationError("فایل زیپ شده ورودی معتبر نمیباشد")

        # Find shapefile in the extracted directory
        gdb_files = [f for f in os.listdir(tmpdirname) if f.endswith('.gdb')]
        if not gdb_files:
            raise GeoDatabaseValidationError("فایلی با پسوند .gdb در فایل زیپ شده ورودی یافت نشد")

        gdb_path = os.path.join(tmpdirname, gdb_files[0])

        try:
            # Get all layers
            layers = fiona.listlayers(gdb_path)
            # Get only layers with rows
            layers_with_rows = []
            for lyr in layers:
                gdf = gpd.read_file(gdb_path, layer=lyr)
                if gdf.empty or len(gdf) == 0:
                    continue
                else:
                    layers_with_rows.append(lyr)
            return layers_with_rows
        except Exception as e:
            print(e)
            raise GeoDatabaseValidationError(f"خطا در خواندن ژیودیتابیس")
        
def get_layersnames_from_zipped_geodatabase_fast(
    gdb_zip_file: InMemoryUploadedFile
) -> List[dict]:  # <-- updated return type
    with tempfile.TemporaryDirectory() as tmpdirname:
        zip_path = os.path.join(tmpdirname, f"gdbzipfile_{uuid.uuid4().hex[:8]}.zip")

        with open(zip_path, "wb+") as f:
            for chunk in gdb_zip_file.chunks():
                f.write(chunk)

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdirname)
        except zipfile.BadZipFile:
            raise GeoDatabaseValidationError("فایل زیپ شده ورودی معتبر نمیباشد")

        gdb_path = None
        for root, dirs, _ in os.walk(tmpdirname):
            for d in dirs:
                if d.endswith(".gdb"):
                    gdb_path = os.path.join(root, d)
                    break
            if gdb_path:
                break

        if not gdb_path:
            raise GeoDatabaseValidationError("فایلی با پسوند .gdb در فایل زیپ شده ورودی یافت نشد")

        # --- Try using ogrinfo CLI first (fast path) ---
        try:
            cmd = ["ogrinfo", gdb_path, "-so", "-ro", "-json"]
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
            data = json.loads(result.stdout)

            layers_with_rows = [
                {
                    "layername": lyr.get("name"),
                    "alias": (
                        lyr.get("metadata", {}).get("", {}).get("ALIAS_NAME")
                        or lyr.get("metadata", {}).get("", {}).get("alias")
                        or lyr.get("alias")
                        or lyr.get("aliasName")
                        or lyr.get("name")
                    ),
                }
                for lyr in data.get("layers", [])
                if lyr.get("featureCount", 0) > 0
            ]

            return layers_with_rows

        except (subprocess.CalledProcessError, FileNotFoundError) as cli_err:
            # --- Fallback: Fiona ---
            print(f"ogrinfo not used or failed: {cli_err}\nFalling back to Fiona.")
            try:
                layers_with_rows = []
                for layer in fiona.listlayers(gdb_path):
                    with fiona.open(gdb_path, layer=layer) as src:
                        if len(src) > 0:
                            alias = (
                                alias
                                or src.meta.get("alias")
                                or src.meta.get("ALIAS_NAME")
                                or src.profile.get("alias")
                                or src.profile.get("ALIAS_NAME")
                                or getattr(src, "alias", None)
                                or layer  # final fallback
                            )
                            layers_with_rows.append({
                                "layername": layer,
                                "alias": alias,
                            })
                return layers_with_rows
            except Exception as e:
                raise GeoDatabaseValidationError(f"خطا در خواندن ژیودیتابیس: {str(e)}")
         
def save_gdbzipfile_into_tempdir_with_uuid(
    gdb_zip_file : InMemoryUploadedFile,
) -> str :
    """
        save the gdbzip file into <media root>/<temp_uploads>/uplodedgdbzipfiles/<uuid>/gdbzip.zip

        Return the uuid as a string
    """
    try:
        this_uuid : str = uuid.uuid4().hex

        # Create the directory structure
        # base_temp_dir = tempfile.gettempdir()
        base_temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
        upload_dir = os.path.join(base_temp_dir, "uplodedgdbzipfiles", this_uuid)
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, "gdbzip.zip")

        # Save the uploaded file
        with open(file_path, 'wb') as destination:
            for chunk in gdb_zip_file.chunks():
                destination.write(chunk)

        return this_uuid
    except Exception as e:
        print(e)
        raise GeoDatabaseValidationError(f"خطا در خواندن ژیودیتابیس")
    
def read_all_layers_from_uuid(
    geodb_uuid:str,
) -> List[str]:
    
    base_temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
    os.makedirs(base_temp_dir, exist_ok=True)  # Ensure directory exists

    file_path = os.path.join(base_temp_dir, "uplodedgdbzipfiles", geodb_uuid, "gdbzip.zip")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"متاسفانه فایل زیپ شده پیدا نشد لطفا مجدد تلاش کنید")

    extraction_dir = os.path.join(base_temp_dir, f"{geodb_uuid}_dir")
    
    try:
        # Extract zip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_dir)
    except zipfile.BadZipFile:
        raise GeoDatabaseValidationError("فایل زیپ شده ورودی معتبر نمیباشد")

    # Find geodatabase file in the extracted directory
    gdb_files = [f for f in os.listdir(extraction_dir) if f.endswith('.gdb')]
    if not gdb_files:
        raise GeoDatabaseValidationError("فایلی با پسوند .gdb در فایل زیپ شده ورودی یافت نشد")

    gdb_path = os.path.join(extraction_dir, gdb_files[0])

    try:
        # Get layer names from the geodatabase
        all_layer_names = fiona.listlayers(gdb_path)
        return all_layer_names
    except Exception as e:
        print(e)
        raise GeoDatabaseValidationError(f"خطا در خواندن ژیودیتابیس")
    
def read_all_layers_from_uuid_fast(geodb_uuid: str) -> List[str]:
    """
    Given a UUID corresponding to an uploaded ZIP containing a FileGDB,
    extract it, locate the .gdb directory, and return *all* layer names.
    Uses ogrinfo (fast) with Fiona fallback.

    Args:
        geodb_uuid (str): UUID of saved geodatabase ZIP.

    Returns:
        List[str]: All layer names inside the FileGDB.
    """

    # Base temp directory for stored ZIP files
    base_temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_uploads")
    os.makedirs(base_temp_dir, exist_ok=True)

    # Path where the uploaded ZIP is expected
    file_path = os.path.join(
        base_temp_dir,
        "uplodedgdbzipfiles",
        geodb_uuid,
        "gdbzip.zip"
    )

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "متاسفانه فایل زیپ شده پیدا نشد لطفا مجدد تلاش کنید"
        )

    # Extraction directory
    extraction_dir = os.path.join(base_temp_dir, f"{geodb_uuid}_dir")

    # Extract ZIP
    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extraction_dir)
    except zipfile.BadZipFile:
        raise GeoDatabaseValidationError("فایل زیپ شده ورودی معتبر نمیباشد")

    # Find .gdb folder (recursive search)
    gdb_path = None
    for root, dirs, _ in os.walk(extraction_dir):
        for d in dirs:
            if d.endswith(".gdb"):
                gdb_path = os.path.join(root, d)
                break
        if gdb_path:
            break

    if not gdb_path:
        raise GeoDatabaseValidationError(
            "فایلی با پسوند .gdb در فایل زیپ شده ورودی یافت نشد"
        )

    # First attempt: use ogrinfo CLI for speed
    try:
        cmd = ["ogrinfo", gdb_path, "-so", "-ro", "-json"]
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        # All layer names (empty or not)
        layer_names = [lyr.get("name") for lyr in data.get("layers", [])]

        return layer_names

    except (subprocess.CalledProcessError, FileNotFoundError) as cli_err:
        # Fallback: Fiona (slower)
        print(f"ogrinfo unavailable or failed: {cli_err}\nFalling back to Fiona.")
        try:
            return fiona.listlayers(gdb_path)
        except Exception as e:
            print(e)
            raise GeoDatabaseValidationError("خطا در خواندن ژیودیتابیس")

    

def process_layer_data_from_gdb(
    geodb_uuid : str ,
    layer_models : List[Any] ,
    shrh_layer_instances : Any ,
) -> Tuple[bool, Optional[List[Dict[str, Any]]], str] :
    
    """
    Process uploaded geodatabase from uuid for multi layer border
    
    Args:
            
    Returns:
        tuple: (success, processed_data, message)
    """

    base_temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
    os.makedirs(base_temp_dir, exist_ok=True)  # Ensure directory exists

    file_path = os.path.join(base_temp_dir, "uplodedgdbzipfiles", geodb_uuid, "gdbzip.zip")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"متاسفانه فایل زیپ شده پیدا نشد لطفا مجدد تلاش کنید")

    extraction_dir = os.path.join(base_temp_dir, f"{geodb_uuid}_dir")
    
    try:
        # Extract zip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extraction_dir)
    except zipfile.BadZipFile:
        raise GeoDatabaseValidationError("فایل زیپ شده ورودی معتبر نمیباشد")

    # Find geodatabase file in the extracted directory
    gdb_files = [f for f in os.listdir(extraction_dir) if f.endswith('.gdb')]
    if not gdb_files:
        raise GeoDatabaseValidationError("فایلی با پسوند .gdb در فایل زیپ شده ورودی یافت نشد")

    gdb_path = os.path.join(extraction_dir, gdb_files[0])

    processed_data = []
    for shrhlyr in shrh_layer_instances:
        gdf = gpd.read_file(gdb_path, layer=shrhlyr.layer_name.layername_en)
        
        # CHECK gdf is peresent or not !!!!!!!!!!!!
        # CHECK IF GDF IS EMPTY - ADD THIS
        if gdf.empty or len(gdf) == 0:
            return False, [], f'لایه {shrhlyr.layer_name.layername_en} خالی است و هیچ رکوردی ندارد'

        # Validate GeoDataFrame using common service
        is_valid, validation_error = validate_geodataframe(gdf , validation_check=False)
        if not is_valid:
            return False, None, f'خطا در اعتبارسنجی لایه {shrhlyr.layer_name.layername_fa}: {validation_error}'

        # Get geometry type from gdf
        try:
            gdf_geometry_type = get_geometry_type(gdf)
        except Exception as e:
            return False, None, f'خطا در تشخیص نوع هندسه {shrhlyr.layer_name.layername_fa} : {str(e)}'

        this_layer_model = next(
            (mdl for mdl in layer_models if mdl.__name__ == shrhlyr.layer_name.layername_en), None
            )
        
        if this_layer_model is None:
            return False , None , f"لایه ایی با نام {shrhlyr.layer_name.layername_fa} در دیتابیس یافت نشد"

        # Find geometry field in the model dynamically
        geometry_field = None
        geometry_field_name = None

        
        for field in this_layer_model._meta.get_fields():
            if isinstance(field, (gis_models.GeometryField, gis_models.PointField, 
                                gis_models.LineStringField, gis_models.PolygonField,
                                gis_models.MultiPointField, gis_models.MultiLineStringField,
                                gis_models.MultiPolygonField)):
                geometry_field = field
                geometry_field_name = field.name
                break
        
        if not geometry_field:
            return False, None, 'فیلد هندسه در مدل یافت نشد'
        
        # Check geometry compatibility
        model_geom_type = type(geometry_field).__name__
        compatibility = check_geometry_compatibility(
            gdf_geometry_type,
            model_geom_type
        )
        
        if not compatibility['compatible']:
            return False, None, compatibility['error_message']
        
        # Convert CRS to EPSG:4326 if needed
        if gdf.crs is None:
            return False, None, f"سیستم مختصات برای لایه {shrhlyr.layer_name.layername_fa} مشخص نیست"
        
        if gdf.crs.to_epsg() != 4326:
            try:
                gdf = gdf.to_crs(epsg=4326)
            except Exception as e:
                return False, None, f"خطا در تبدیل سیستم مختصات برای لایه {shrhlyr.layer_name.layername_fa}: {str(e)}"
        
        # Process features
        # print("><><>>>>>" , gdf)
        feature_data = {'shrhlyr': shrhlyr,'rows':[]}
        for idx, row in gdf.iterrows():
            this_row = {'shr_layer':shrhlyr}
            geometry = row.geometry
            
            if geometry is None or geometry.is_empty:
                return False, None, f"هندسه خالی در ردیف {idx + 1} برای لایه {shrhlyr.layer_name.layername_fa} یافت شد"
            
            # Convert geometry to appropriate Django geometry type
            try:
                django_geom = convert_geometry_to_django(geometry, model_geom_type)
                this_row[geometry_field_name] = django_geom
            except Exception as e:
                return False, None, f"خطا در تبدیل هندسه در ردیف  {idx + 1} برای لایه {shrhlyr.layer_name.layername_fa}: {str(e)}"

            normalize_db_fields = {f.name.lower(): f.name for f in this_layer_model._meta.get_fields()}

            normalize_gdf_cols = {col.lower(): col for col in gdf.columns}

            for lower_db_field , original_db_filed in normalize_db_fields.items():
                
                if lower_db_field not in normalize_gdf_cols:
                    continue

                original_gdf_col_name = normalize_gdf_cols[lower_db_field]

                value = row[original_gdf_col_name]

                if pd.isna(value):
                    value = None

                try:
                    model_field = this_layer_model._meta.get_field(original_db_filed)
                    converted_value = convert_field_value(value , model_field)
                    this_row[original_db_filed] = converted_value
                except Exception as e:
                    return False, None, f"خطا در تبدیل فیلد {original_db_filed} برای لایه {shrhlyr.layer_name.layername_fa}: {str(e)}"
                
            feature_data['rows'].append(this_row)
        
        processed_data.append(feature_data)

    return True , processed_data , "ok"

