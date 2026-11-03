import os
import zipfile
import tempfile
import json
import uuid
import traceback

from django.apps import apps
from django.db import models
from django.contrib.gis.db import models as gis_models


from layers.apps import LayersConfig

import fiona
import pyogrio
from geopandas import GeoDataFrame

import logging

from django.core.management.base import BaseCommand

# logging.getLogger('fiona').setLevel(logging.ERROR)

class Command(BaseCommand):
    help = 'Check Template Geodatabase file with Database'

    def add_arguments(self, parser):
        parser.add_argument(
            'gdb_file',
            type=str,
            help='Path to GeoDatabase file for Compare (in zip)'
        )

    def get_geometry_type_from_field(self, field):
        """Get geometry type string from Django GIS field"""
        if isinstance(field, gis_models.MultiPolygonField):
            return 'MultiPolygon'
        elif isinstance(field, gis_models.PolygonField):
            return 'Polygon'
        elif isinstance(field, gis_models.MultiLineStringField):
            return 'MultiLineString'
        elif isinstance(field, gis_models.LineStringField):
            return 'LineString'
        elif isinstance(field, gis_models.MultiPointField):
            return 'MultiPoint'
        elif isinstance(field, gis_models.PointField):
            return 'Point'
        elif isinstance(field, gis_models.GeometryCollectionField):
            return 'GeometryCollection'
        return None

    # def get_fiona_geometry_type(self, layer_path, layer_name):
    #     """Get geometry type from geodatabase layer using fiona"""
    #     try:
    #         sql = f"SELECT * FROM {layer_name}"
    #         with fiona.open(layer_path, layer=layer_name , sql=sql) as src:
    #             # Get geometry type from schema
    #             geom_type = src.schema.get('geometry')
    #             if geom_type:
    #                 # Fiona returns types like 'Polygon', 'MultiPolygon', etc.
    #                 return geom_type
    #             return None
    #     except Exception as e:
    #         return None
    def get_pyogrio_geometry_type(self, gdb_path, layer_name):
        try:
            info = pyogrio.read_info(gdb_path, layer=layer_name)
            return info.get('geometry_type')
        except Exception:
            return None

    # def get_fiona_fields(self, layer_path, layer_name):
    #     """Get field names and types from geodatabase layer using fiona (skip default GDB fields)"""
    #     # Default GDB fields to skip
    #     skip_fields = ['SHAPE_Area', 'SHAPE_Length', 'SHAPE_area', 'SHAPE_length', 'Shape_Area', 'Shape_Length']
        
    #     try:
    #         with fiona.open(layer_path, layer=layer_name , driver="FileGDB") as src:
    #             # Get properties (fields) from schema
    #             properties = src.schema.get('properties', {})

    #             print(f"----------Layer: {layer_name}")
    #             print(f"  Schema: { src.schema }")
    #             print(f"  Fields: {list(src.schema['properties'].keys())}")
    #             print(f"  Geometry: {src.schema['geometry']}")
    #             print(f"----------Layer: {layer_name}")
    #             # Filter out default GDB fields
    #             filtered_properties = {}
    #             for field_name, field_type in properties.items():
    #                 if field_name not in skip_fields:
    #                     # if field_name.endswith("_"):
    #                         # field_name = field_name[:-1]
    #                     filtered_properties[field_name] = field_type

    #                     print(f"--Filtered properties for layers {layer_name} :  {filtered_properties}")
    #             return filtered_properties
    #     except Exception as e:
    #         return {}
    def map_pyogrio_dtype(self, dtype):
        """Convert pyogrio/numpy dtype to simple type string matching Django mapping"""
        dtype = str(dtype).lower()
        
        # String/text types
        if dtype in ('object', 'str', 'string', 'text', 'varchar', 'unicode'):
            return 'str'
        
        # Integer types
        if dtype in ('int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32', 'uint64', 'int'):
            return 'int'
        
        # Float/decimal types
        if dtype in ('float16', 'float32', 'float64', 'float', 'double', 'real'):
            return 'float'
        
        # Boolean
        if dtype == 'bool':
            return 'bool'
        
        # Date/time
        if dtype in ('datetime64', 'datetime', 'timestamp'):
            return 'datetime'
        
        # Default fallback
        return 'str'
    def get_pyogrio_fields(self, gdb_path, layer_name):
        skip_fields = ['SHAPE_Area', 'SHAPE_Length', 'SHAPE_area', 'SHAPE_length', 'Shape_Area', 'Shape_Length']
        try:
            info = pyogrio.read_info(gdb_path, layer=layer_name)
            fields = info['fields']   # array of field names
            dtypes = info['dtypes']   # array of dtype strings
            filtered = {}
            for name, dtype in zip(fields, dtypes):
                if name in skip_fields:
                    continue
                # Remove trailing underscore if present (to match Django field names)
                cleaned_name = name.rstrip('_')
                # filtered[cleaned_name] = dtype
                filtered[cleaned_name] = self.map_pyogrio_dtype(dtype)
            return filtered
        except Exception as e:
            return {}

    def get_django_model_fields(self, model_class):
        """Get field names and types from Django model (excluding geometry fields and auto fields)"""
        fields = {}
        for field in model_class._meta.get_fields():
            # Skip geometry fields (border), auto fields, reverse relations, and many-to-many
            if field.name == 'border':
                continue
            if field.auto_created:
                continue
            if field.is_relation and not field.many_to_many:
                continue
            
            # Map Django field types to Fiona/OGR types
            field_type = self.map_django_field_to_ogr(field)
            if field_type:
                fields[field.name] = field_type
        
        return fields

    def map_django_field_to_ogr(self, field):
        """Map Django field types to Fiona/OGR field types"""
        from django.db import models as django_models
        
        if isinstance(field, (django_models.CharField, django_models.TextField)):
            return 'str'
        elif isinstance(field, django_models.IntegerField):
            return 'int'
        elif isinstance(field, django_models.FloatField):
            return 'float'
        elif isinstance(field, django_models.DecimalField):
            return 'float'
        elif isinstance(field, django_models.BooleanField):
            return 'int'  # Boolean fields are often stored as integers in shapefiles
        elif isinstance(field, django_models.DateField):
            return 'date'
        elif isinstance(field, django_models.DateTimeField):
            return 'datetime'
        elif isinstance(field, django_models.TimeField):
            return 'time'
        elif isinstance(field, django_models.JSONField):
            return 'str'  # JSON fields can be stored as strings
        elif isinstance(field, django_models.EmailField):
            return 'str'
        elif isinstance(field, django_models.URLField):
            return 'str'
        elif isinstance(field, django_models.SlugField):
            return 'str'
        elif isinstance(field, django_models.UUIDField):
            return 'str'
        elif isinstance(field, django_models.ForeignKey):
            return 'int'  # Foreign keys are stored as integers
        else:
            return 'str'  # Default to string for unknown types

    def handle(self, *args, **options):
        gdb_file = options['gdb_file']
        
        if not os.path.exists(gdb_file):
            self.stdout.write(self.style.ERROR(f'File not found: {gdb_file}'))
            return

        # Open GDB file
        base_temp_dir = tempfile.gettempdir()
        uid = uuid.uuid4()
        extraction_dir = os.path.join(base_temp_dir, f"{uid}_dir")

        try:
            # Extract zip file
            with zipfile.ZipFile(gdb_file, 'r') as zip_ref:
                zip_ref.extractall(extraction_dir)
        except zipfile.BadZipFile:
            self.stdout.write(self.style.ERROR(f'فایل زیپ شده معتبر نمیباشد'))
            return

        # Find geodatabase file in the extracted directory
        gdb_files = [f for f in os.listdir(extraction_dir) if f.endswith('.gdb')]
        if not gdb_files:
            self.stdout.write(self.style.ERROR(f"فایلی با پسوند .gdb در فایل زیپ شده ورودی یافت نشد"))
            return

        gdb_path = os.path.join(extraction_dir, gdb_files[0])

        # List of all layers from geodatabase
        try:
            # Get layer names from the geodatabase
            # all_gdb_layer_names = fiona.listlayers(gdb_path)
            layers_info = pyogrio.list_layers(gdb_path)  # returns list of [name, geometry_type]
            all_gdb_layer_names = [item[0] for item in layers_info]  # extract just names
        except Exception as e:
            error_trace = traceback.format_exc()
            print(error_trace)
            self.stdout.write(self.style.ERROR(f'خطای غیر منتظره در پردازش زیپ فایل'))
            return

        # Get All Database Layers
        try:
            all_layer_model_class = apps.all_models[LayersConfig.name]
        except (ValueError, LookupError) as e:
            self.stdout.write(self.style.ERROR(f"Failed to get all models from app '{LayersConfig.name}': {e}"))
            return

        # Create a case-insensitive mapping for geodatabase layer names
        gdb_layer_names_lower = {name.lower(): name for name in all_gdb_layer_names}

        # Get model names and their border field geometry types
        database_models_info = {}
        for model_name, model_class in all_layer_model_class.items():
            # Check if model has a database table and has border field
            if hasattr(model_class, '_meta') and model_class._meta.db_table:
                # Find the border field
                border_field = None
                for field in model_class._meta.get_fields():
                    if field.name == 'border':
                        border_field = field
                        break
                
                # Get all fields from Django model (excluding border)
                django_fields = self.get_django_model_fields(model_class)
                
                if border_field:
                    geom_type = self.get_geometry_type_from_field(border_field)
                    if geom_type:
                        database_models_info[model_name] = {
                            'model_class': model_class,
                            'border_field': border_field,
                            'expected_geom_type': geom_type,
                            'django_fields': django_fields
                        }
                    else:
                        database_models_info[model_name] = {
                            'model_class': model_class,
                            'border_field': border_field,
                            'expected_geom_type': 'Unknown',
                            'django_fields': django_fields
                        }
                else:
                    database_models_info[model_name] = {
                        'model_class': model_class,
                        'border_field': None,
                        'expected_geom_type': 'No border field',
                        'django_fields': django_fields
                    }
        
        self.stdout.write(f"Found {len(database_models_info)} models in database with border field")
        
        # Check for existing layers and verify geometry types and fields
        geometry_matches = []
        geometry_mismatches = []
        missing_layers = []
        no_border_field_layers = []
        field_matches = []
        field_mismatches = []
        
        # Store field issues per model
        model_field_issues = {}
        
        for db_model, model_info in database_models_info.items():
            # Case-insensitive check
            db_model_lower = db_model.lower()
            if db_model_lower not in gdb_layer_names_lower:
                missing_layers.append(db_model)
                continue
            
            # Get the actual layer name from geodatabase (original case)
            actual_gdb_layer_name = gdb_layer_names_lower[db_model_lower]
            
            # Check if model has border field
            if model_info['border_field'] is None:
                no_border_field_layers.append(db_model)
                continue
            
            # Get geometry type from geodatabase
            # gdb_geom_type = self.get_fiona_geometry_type(gdb_path, actual_gdb_layer_name)
            gdb_geom_type = self.get_pyogrio_geometry_type(gdb_path, actual_gdb_layer_name)
            
            if gdb_geom_type is None:
                geometry_mismatches.append({
                    'model': db_model,
                    'expected': model_info['expected_geom_type'],
                    'actual': 'Unable to read geometry'
                })
                continue
            
            # Compare geometry types
            expected = model_info['expected_geom_type'].lower()
            actual = gdb_geom_type.lower()
            
            is_match = False
            if expected == actual:
                is_match = True
            elif expected == 'multipolygon' and actual == 'polygon':
                is_match = True
            elif expected == 'multilinestring' and actual == 'linestring':
                is_match = True
            elif expected == 'multipoint' and actual == 'point':
                is_match = True
            
            if is_match:
                geometry_matches.append({
                    'model': db_model,
                    'expected': model_info['expected_geom_type'],
                    'actual': gdb_geom_type
                })
            else:
                geometry_mismatches.append({
                    'model': db_model,
                    'expected': model_info['expected_geom_type'],
                    'actual': gdb_geom_type
                })
            
            # Compare fields
            # gdb_fields = self.get_fiona_fields(gdb_path, actual_gdb_layer_name)
            gdb_fields = self.get_pyogrio_fields(gdb_path, actual_gdb_layer_name)
            
            # print(f"--- DEBUG: GDB fields for {actual_gdb_layer_name}: {gdb_fields}")

            # Create case-insensitive mapping for GDB fields
            gdb_fields_lower = {field_name.lower(): {'name': field_name, 'type': field_type} 
                                for field_name, field_type in gdb_fields.items()}
            
            # Check Django fields against GDB fields
            django_field_names_lower = {field_name.lower(): field_name for field_name in model_info['django_fields'].keys()}
            
            # Collect issues for this model
            missing = []
            extra = []
            mismatches = []
            
            # Find missing fields (in Django but not in GDB)
            for django_field_lower, django_field_original in django_field_names_lower.items():
                if django_field_lower not in gdb_fields_lower:
                    missing.append({
                        'field': django_field_original,
                        'type': model_info['django_fields'][django_field_original]
                    })
            
            # Find extra fields (in GDB but not in Django)
            for gdb_field_lower, gdb_field_info in gdb_fields_lower.items():
                if gdb_field_lower not in django_field_names_lower:
                    extra.append({
                        'field': gdb_field_info['name'],
                        'type': gdb_field_info['type']
                    })
            
            # Check field type compatibility for common fields
            for django_field_lower, django_field_original in django_field_names_lower.items():
                if django_field_lower in gdb_fields_lower:
                    django_type = model_info['django_fields'][django_field_original]
                    gdb_type = gdb_fields_lower[django_field_lower]['type']
                    
                    # Check if types are compatible
                    type_compatible = self.are_field_types_compatible(django_type, gdb_type)
                    
                    if not type_compatible:
                        mismatches.append({
                            'field': django_field_original,
                            'django_type': django_type,
                            'gdb_type': gdb_type
                        })
                    else:
                        field_matches.append({
                            'model': db_model,
                            'field': django_field_original,
                            'django_type': django_type,
                            'gdb_type': gdb_type
                        })
            
            # Store issues for this model if any
            if missing or extra or mismatches:
                model_field_issues[db_model] = {
                    'missing': missing,
                    'extra': extra,
                    'mismatches': mismatches
                }
            
            # Add mismatches to the global list
            for mismatch in mismatches:
                field_mismatches.append({
                    'model': db_model,
                    'field': mismatch['field'],
                    'django_type': mismatch['django_type'],
                    'gdb_type': mismatch['gdb_type']
                })
        
        # Results
        self.stdout.write("\n" + "="*70)
        self.stdout.write("GEOMETRY TYPE COMPARISON RESULTS")
        self.stdout.write("="*70)
        
        # Summary
        self.stdout.write(f"\n📊 Summary:")
        self.stdout.write(f"  - Total database models: {len(database_models_info)}")
        self.stdout.write(f"  - Models with border field: {len([m for m in database_models_info.values() if m['border_field'] is not None])}")
        self.stdout.write(f"  - Layers found in GDB: {len(geometry_matches) + len(geometry_mismatches)}")
        self.stdout.write(f"  - Missing layers: {len(missing_layers)}")
        self.stdout.write(f"  - Models without border field: {len(no_border_field_layers)}")
        
        # Geometry matches
        if geometry_matches:
            self.stdout.write(f"\n✅ Geometry MATCHES ({len(geometry_matches)}):")
            for item in geometry_matches:
                self.stdout.write(self.style.SUCCESS(f"  ✓ {item['model']}: {item['expected']} == {item['actual']}"))
        
        # Geometry mismatches
        if geometry_mismatches:
            self.stdout.write(f"\n❌ Geometry MISMATCHES ({len(geometry_mismatches)}):")
            for item in geometry_mismatches:
                self.stdout.write(self.style.ERROR(f"  ✗ {item['model']}: Expected '{item['expected']}' but got '{item['actual']}'"))
        
        # Field comparison results in compact format
        if model_field_issues:
            self.stdout.write("\n" + "="*70)
            self.stdout.write(f"with field issue numbers: {len(model_field_issues)}")
            self.stdout.write("FIELD COMPARISON RESULTS")
            self.stdout.write("="*70)
            
            for model, issues in model_field_issues.items():
                self.stdout.write(f"\n📁 {model}:")
                
                # Missing fields (in Django but not in GDB) - Yellow color
                if issues['missing']:
                    missing_fields_str = ', '.join([f"{item['field']}({item['type']})" for item in issues['missing']])
                    self.stdout.write(self.style.WARNING(f"  ⚠️ Missing: {missing_fields_str}"))
                
                # Extra fields (in GDB but not in Django) - Cyan/Blue color
                if issues['extra']:
                    extra_fields_str = ', '.join([f"{item['field']}({item['type']})" for item in issues['extra']])
                    self.stdout.write(self.style.NOTICE(f"  📌 Extra: {extra_fields_str}"))
                
                # Type mismatches - Red color
                if issues['mismatches']:
                    mismatch_fields_str = ', '.join([f"{item['field']}(Django:{item['django_type']}≠GDB:{item['gdb_type']})" for item in issues['mismatches']])
                    self.stdout.write(self.style.ERROR(f"  ❌ Type mismatch: {mismatch_fields_str}"))
            
            # Also show field matches summary if there are many
            if field_matches and len(field_matches) > 0:
                self.stdout.write(f"\n✅ Field type matches: {len(field_matches)} fields matched correctly")
        
        # Missing layers
        if missing_layers:
            self.stdout.write(f"\n⚠️  Missing layers in geodatabase ({len(missing_layers)}):")
            for layer in missing_layers:
                self.stdout.write(self.style.WARNING(f"  - {layer}"))
        
        # Models without border field
        if no_border_field_layers:
            self.stdout.write(f"\nℹ️  Models without border field ({len(no_border_field_layers)}):")
            for layer in no_border_field_layers:
                self.stdout.write(f"  - {layer}")
        
        # Extra layers in geodatabase
        db_models_lower = set(database_models_info.keys())
        extra_layers_case_insensitive = []
        for gdb_layer in all_gdb_layer_names:
            if gdb_layer.lower() not in {db_model.lower() for db_model in db_models_lower}:
                extra_layers_case_insensitive.append(gdb_layer)
        
        if extra_layers_case_insensitive:
            self.stdout.write(f"\n📌 Extra layers in geodatabase not in database ({len(extra_layers_case_insensitive)}):")
            for layer in extra_layers_case_insensitive:
                # geom_type = self.get_fiona_geometry_type(gdb_path, layer)
                geom_type = self.get_pyogrio_geometry_type(gdb_path, layer)
                self.stdout.write(f"  - {layer} ({geom_type if geom_type else 'Unknown geometry'})")
        
        self.stdout.write("\n" + "="*70)
        
        # Final status
        if geometry_mismatches or missing_layers or field_mismatches or model_field_issues:
            self.stdout.write(self.style.ERROR("\n❌ VALIDATION FAILED: Some geometry types, fields, or layers don't match"))
        elif geometry_matches and not geometry_mismatches and not missing_layers and not field_mismatches:
            self.stdout.write(self.style.SUCCESS("\n✅ VALIDATION PASSED: All geometry types and fields match correctly!"))
        else:
            self.stdout.write(self.style.WARNING("\n⚠️ VALIDATION COMPLETED WITH WARNINGS"))

    def are_field_types_compatible(self, django_type, gdb_type):
        """Check if Django field type is compatible with Fiona/GDB field type"""
        # Convert both to lowercase for comparison
        django_type = django_type.lower()
        gdb_type = str(gdb_type).lower()
        
        # Extract base type from GDB type (remove anything after colon or space)
        # Examples: 'str:50' -> 'str', 'int:10' -> 'int', 'float:15.5' -> 'float'
        if ':' in gdb_type:
            gdb_base_type = gdb_type.split(':')[0]
        elif ' ' in gdb_type:
            gdb_base_type = gdb_type.split(' ')[0]
        else:
            gdb_base_type = gdb_type
        
        # Also handle cases like 'int16', 'int32', 'int64' -> 'int'
        if gdb_base_type.startswith('int'):
            gdb_base_type = 'int'
        elif gdb_base_type.startswith('float') or gdb_base_type.startswith('double'):
            gdb_base_type = 'float'
        elif gdb_base_type.startswith('str') or gdb_base_type.startswith('string') or gdb_base_type.startswith('text'):
            gdb_base_type = 'str'
        elif gdb_base_type.startswith('date'):
            gdb_base_type = 'date'
        elif gdb_base_type.startswith('time'):
            gdb_base_type = 'time'
        
        # Define compatible type mappings
        compatible_types = {
            'str': ['str', 'string', 'text', 'varchar', 'char'],
            'int': ['int', 'integer', 'long', 'int64', 'int32', 'int16'],
            'float': ['float', 'double', 'real', 'decimal', 'numeric'],
            'date': ['date', 'str', 'string', 'text', 'varchar', 'char'],
            'datetime': ['datetime', 'timestamp', 'str', 'string', 'text', 'varchar', 'char'],
            'time': ['time', 'str', 'string', 'text', 'varchar', 'char'],
            'bool': ['int', 'integer', 'bool', 'boolean']
        }
        # Check compatibility
        if django_type in compatible_types:
            return gdb_base_type in compatible_types[django_type]
        
        # If django_type is 'str' (default), consider it compatible with most types
        if django_type == 'str':
            return gdb_base_type not in ['geometry', 'point', 'linestring', 'polygon', 'multipolygon']
        
        return django_type == gdb_base_type