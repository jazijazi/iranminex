import psycopg2
from django.apps import apps
from django.db import transaction

def layer_transferer():
    """
    Transfer data from old database tables to new LinkedToLayerTable models
    """
    # Get all models from the 'layers' app
    layers_app_models = apps.get_app_config('layers').get_models()
    
    # Import necessary models
    from layers.models.models import LinkedToLayerTable
    from contracts.models.models import ShrhLayer, ShrhBase, Contract
    
    # Connect to the old database
    try:
        old_db_conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='zarrinold',
            user='jazi',
            password='137474'
        )
        old_db_cursor = old_db_conn.cursor()
        print("✓ Connected to old database (zarrinold)")
    except Exception as e:
        print(f"✗ Failed to connect to old database: {e}")
        return
    
    print("=" * 80)
    print("Building mapping: ProjectGharar -> ShrhLayer")
    print("=" * 80)
    
    # Step 1: Build mapping from old ProjectGharar ID to new ShrhLayer ID
    # This requires understanding your business logic for mapping
    prjgharar_to_shrhlayer_map = build_prjgharar_to_shrhlayer_mapping(old_db_cursor)
    
    if not prjgharar_to_shrhlayer_map:
        print("✗ Failed to build mapping. Cannot proceed with transfer.")
        old_db_cursor.close()
        old_db_conn.close()
        return
    
    print(f"✓ Built mapping for {len(prjgharar_to_shrhlayer_map)} ProjectGharar records")
    print("=" * 80)
    print("Starting data transfer...")
    print("=" * 80)
    
    found_count = 0
    total_transferred = 0
    
    for model in layers_app_models:
        if issubclass(model, LinkedToLayerTable):
            found_count += 1
            model_name = model.__name__
            new_table_name = model._meta.db_table
            old_table_name = new_table_name.replace('layers_', 'prjapi_')
            
            # Transfer data for this model
            transferred = transfer_model_data(
                model=model,
                old_table_name=old_table_name,
                old_db_cursor=old_db_cursor,
                prjgharar_to_shrhlayer_map=prjgharar_to_shrhlayer_map
            )
            
            total_transferred += transferred
            
            print(f"\n{found_count}. Model: {model_name}")
            print(f"   Table: {new_table_name}")
            print(f"   Transferred: {transferred} rows")
            print("-" * 80)
    
    # Close old database connection
    old_db_cursor.close()
    old_db_conn.close()
    
    print(f"\n{'=' * 80}")
    print(f"Total models processed: {found_count}")
    print(f"Total rows transferred: {total_transferred}")
    print("=" * 80)


def build_prjgharar_to_shrhlayer_mapping(old_db_cursor):
    """
    Build mapping between old ProjectGharar IDs and new ShrhLayer IDs
    
    The logic here depends on your business requirements:
    - Option 1: Match by layer name and contract
    - Option 2: Match by Sharhkadamat records
    - Option 3: Custom logic based on your needs
    """
    from contracts.models.models import ShrhLayer, ShrhBase, Contract, ContractBorder
    from layers.models.models import LayersNames
    
    mapping = {}
    
    try:
        # Get old Sharhkadamat records which link ProjectGharar to Layers
        old_db_cursor.execute("""
            SELECT 
                sk.id,
                sk.prjgharar_id,
                sk.layer_id,
                l.layername_en,
                l.layername_fa,
                pg.project_id,
                pg.gharardad_id,
                gh.titlegh
            FROM prjapi_sharhkadamat sk
            JOIN prjapi_layers l ON sk.layer_id = l.id
            JOIN prjapi_projectgharar pg ON sk.prjgharar_id = pg.id
            JOIN prjapi_gharardad gh ON pg.gharardad_id = gh.id
            WHERE sk.prjgharar_id IS NOT NULL
        """)
        
        sharhkadamat_records = old_db_cursor.fetchall()
        
        print(f"Found {len(sharhkadamat_records)} Sharhkadamat records in old database")
        
        for record in sharhkadamat_records:
            (sk_id, prjgharar_id, layer_id, layername_en, layername_fa,
             project_id, gharardad_id, gharardad_title) = record
            
            # Try to find matching ShrhLayer in new database
            try:
                # Find contract by title (adjust field name if needed)
                contract = Contract.objects.get(title=gharardad_title)
                
                # Find LayersNames that matches the old layer
                # Match by layername_en or layername_fa (whichever is more reliable)
                layer_name = None
                if layername_en:
                    layer_name = LayersNames.objects.filter(layername_en=layername_en).first()
                if not layer_name and layername_fa:
                    layer_name = LayersNames.objects.filter(layername_fa=layername_fa).first()
                
                if not layer_name:
                    print(f"  ⚠ LayerName not found for en='{layername_en}', fa='{layername_fa}'")
                    continue
                
                # Find ShrhLayer that matches the layer name and contract
                shrh_layer = ShrhLayer.objects.filter(
                    layer_name=layer_name,
                    shrh_base__contract=contract
                ).first()
                
                if shrh_layer:
                    mapping[prjgharar_id] = shrh_layer.id
                    print(f"  ✓ Mapped ProjectGharar {prjgharar_id} -> ShrhLayer {shrh_layer.id} (layer: {layername_en or layername_fa}, contract: {gharardad_title})")
                else:
                    print(f"  ⚠ No matching ShrhLayer found for ProjectGharar {prjgharar_id} (layer: {layername_en or layername_fa}, contract: {gharardad_title})")
            
            except Contract.DoesNotExist:
                print(f"  ⚠ Contract not found: {gharardad_title}")
            except Exception as e:
                print(f"  ✗ Error mapping ProjectGharar {prjgharar_id}: {e}")
        
    except Exception as e:
        print(f"✗ Error building mapping: {e}")
        import traceback
        traceback.print_exc()
        return {}
    
    return mapping


def transfer_model_data(model, old_table_name, old_db_cursor, prjgharar_to_shrhlayer_map):
    """
    Transfer data from old table to new model with detailed error reporting
    """
    from django.db import transaction
    
    transferred_count = 0
    skipped_count = 0
    error_count = 0
    
    try:
        # Check if old table exists
        try:
            old_db_cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{old_table_name}'
                )
            """)
            if not old_db_cursor.fetchone()[0]:
                print(f"  ⚠ Table {old_table_name} does not exist in old database")
                return 0
        except Exception as e:
            # Rollback the old database transaction if there's an error
            old_db_cursor.connection.rollback()
            print(f"  ✗ Error checking table existence: {e}")
            return 0
        
        # Get column names from old table
        try:
            old_db_cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{old_table_name}'
                ORDER BY ordinal_position
            """)
            old_columns = [row[0] for row in old_db_cursor.fetchall()]
        except Exception as e:
            old_db_cursor.connection.rollback()
            print(f"  ✗ Error getting columns: {e}")
            return 0
        
        # Get field names from Django model (excluding relations)
        model_field_names = set()
        for f in model._meta.get_fields():
            if not f.many_to_many and not f.one_to_many:
                if hasattr(f, 'attname'):  # ForeignKey uses attname (e.g., 'shr_layer_id')
                    model_field_names.add(f.attname)
                else:
                    model_field_names.add(f.name)
        
        print(f"  Model fields: {sorted(model_field_names)}")
        print(f"  Old table columns: {sorted(old_columns)}")
        
        # Exclude columns
        exclude_columns = {'id', 'rprjgharar_id'}
        data_columns = [col for col in old_columns 
                       if col not in exclude_columns and col in model_field_names]
        
        print(f"  Columns to transfer: {data_columns}")
        
        # Get all rows with rprjgharar_id
        if not data_columns:
            print("  ⚠ No matching columns to transfer")
            return 0
            
        try:
            columns_str = ', '.join(['id', 'rprjgharar_id'] + data_columns)
            old_db_cursor.execute(f"""
                SELECT {columns_str}
                FROM {old_table_name}
                WHERE rprjgharar_id IS NOT NULL
            """)
            old_rows = old_db_cursor.fetchall()
        except Exception as e:
            old_db_cursor.connection.rollback()
            print(f"  ✗ Error fetching data: {e}")
            return 0
        
        if not old_rows:
            print("  No rows with rprjgharar_id found")
            return 0
        
        print(f"  Found {len(old_rows)} rows to transfer")
        
        # Transfer data
        for idx, row in enumerate(old_rows):
            try:
                with transaction.atomic():
                    old_id = row[0]
                    old_prjgharar_id = row[1]
                    old_data = row[2:]
                    
                    # Get new shr_layer_id from mapping
                    new_shr_layer_id = prjgharar_to_shrhlayer_map.get(old_prjgharar_id)
                    
                    if not new_shr_layer_id:
                        skipped_count += 1
                        if skipped_count <= 5:  # Only print first 5 to avoid spam
                            print(f"    ⚠ Skipping old_id={old_id}: No mapping for prjgharar_id={old_prjgharar_id}")
                        continue
                    
                    # Build data dictionary
                    data_dict = {'shr_layer_id': new_shr_layer_id}
                    for col_name, col_value in zip(data_columns, old_data):
                        if col_value is not None:
                            data_dict[col_name] = col_value
                    
                    # Create new record
                    model.objects.create(**data_dict)
                    transferred_count += 1
                    
                    if transferred_count % 100 == 0:
                        print(f"    Progress: {transferred_count}/{len(old_rows)} rows transferred")
                    
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Only print first 5 errors
                    print(f"    ✗ Error with old_id={old_id}: {type(e).__name__}: {e}")
                    if 'data_dict' in locals():
                        print(f"       Data attempted: {data_dict}")
        
        print(f"  Final Summary: Transferred={transferred_count}, Skipped={skipped_count}, Errors={error_count}")
        
    except Exception as e:
        print(f"  ✗ Fatal error for {model.__name__}: {e}")
        import traceback
        traceback.print_exc()
        # Try to rollback old db connection
        try:
            old_db_cursor.connection.rollback()
        except:
            pass
        return 0
    
    return transferred_count