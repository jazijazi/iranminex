import psycopg2
import os
import shutil
from django.db import transaction
from django.conf import settings
from django.core.files import File

def transfer_initialborder_attachments():
    """
    Transfer TarhAttachment data from old database to InitialBorderAttachment in new database
    Including physical file migration from separate old media location
    """
    
    # Import the new models
    from contracts.models import InitialBorderAttachment, InitialBorder, InitialBorderAttachmentDomain
    
    # Define old media root (separate location)
    OLD_MEDIA_ROOT = '/var/mediabck'
    
    # Connect to old database
    try:
        old_conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='zarrinold',
            user='jazi',
            password='137474'
        )
        old_conn.autocommit = True
        old_cursor = old_conn.cursor()
        print("✓ Connected to old database (zarrinold)")
    except Exception as e:
        print(f"✗ Failed to connect to old database: {e}")
        return
    
    print("=" * 80)
    print("Starting TarhAttachment Transfer")
    print(f"Old media location: {OLD_MEDIA_ROOT}")
    print(f"New media location: {settings.MEDIA_ROOT}")
    print("=" * 80)
    
    # Step 1: Build mapping from old Tarh to new InitialBorder
    print("\nStep 1: Building Tarh -> InitialBorder mapping...")
    tarh_mapping = {}
    
    try:
        old_cursor.execute("""
            SELECT t.id, t.titleprj, t.dtarh_id, dt.codetarh
            FROM prjapi_tarh t
            LEFT JOIN prjapi_dtarh dt ON t.dtarh_id = dt.id
        """)
        old_tarh_records = old_cursor.fetchall()
        
        print(f"Found {len(old_tarh_records)} Tarh records in old database")
        
        for old_id, titleprj, dtarh_id, codetarh in old_tarh_records:
            try:
                # Try to find matching InitialBorder by title
                new_border = InitialBorder.objects.filter(title=titleprj).first()
                
                if new_border:
                    tarh_mapping[old_id] = new_border.id
                    print(f"  ✓ Mapped Tarh {old_id} ('{titleprj}') -> InitialBorder {new_border.id}")
                else:
                    print(f"  ⚠ No matching InitialBorder found for Tarh {old_id} ('{titleprj}')")
            
            except Exception as e:
                print(f"  ✗ Error mapping Tarh {old_id}: {e}")
        
        print(f"\n✓ Successfully mapped {len(tarh_mapping)} Tarh records")
    
    except Exception as e:
        print(f"✗ Error building Tarh mapping: {e}")
        import traceback
        traceback.print_exc()
        old_cursor.close()
        old_conn.close()
        return
    
    # Step 2: Build mapping from old DTarhAttachment to new InitialBorderAttachmentDomain
    print("\n" + "=" * 80)
    print("Step 2: Building DTarhAttachment -> InitialBorderAttachmentDomain mapping...")
    print("=" * 80)
    
    dtarh_attach_mapping = {}
    
    try:
        old_cursor.execute("""
            SELECT id, code, name
            FROM prjapi_dtarhattachment
        """)
        old_dtarh_attach_records = old_cursor.fetchall()
        
        print(f"Found {len(old_dtarh_attach_records)} DTarhAttachment records")
        
        for old_id, code, name in old_dtarh_attach_records:
            try:
                # Find matching InitialBorderAttachmentDomain by code
                new_attach_domain = InitialBorderAttachmentDomain.objects.filter(code=code).first()
                
                if new_attach_domain:
                    dtarh_attach_mapping[old_id] = new_attach_domain.id
                    print(f"  ✓ Mapped DTarhAttachment {old_id} (code={code}) -> InitialBorderAttachmentDomain {new_attach_domain.id}")
                else:
                    print(f"  ⚠ No matching InitialBorderAttachmentDomain found for code {code}")
            
            except Exception as e:
                print(f"  ✗ Error mapping DTarhAttachment {old_id}: {e}")
        
        print(f"\n✓ Successfully mapped {len(dtarh_attach_mapping)} DTarhAttachment records")
    
    except Exception as e:
        print(f"✗ Error building DTarhAttachment mapping: {e}")
        import traceback
        traceback.print_exc()
        old_cursor.close()
        old_conn.close()
        return
    
    # Step 3: Transfer TarhAttachment records with files
    print("\n" + "=" * 80)
    print("Step 3: Transferring TarhAttachment records with files...")
    print("=" * 80)
    
    transferred = 0
    skipped = 0
    errors = 0
    file_errors = 0
    
    # Get MEDIA_ROOT for new file operations
    new_media_root = settings.MEDIA_ROOT
    
    try:
        old_cursor.execute("""
            SELECT 
                id,
                upload_date,
                writed_date,
                rtarh_id,
                dtyp_attach_id,
                file
            FROM prjapi_tarhattachment
        """)
        
        old_attachments = old_cursor.fetchall()
        total_records = len(old_attachments)
        
        print(f"\nFound {total_records} TarhAttachment records to transfer")
        
        if total_records == 0:
            print("No records to transfer")
            old_cursor.close()
            old_conn.close()
            return
        
        for old_id, upload_date, writed_date, rtarh_id, dtyp_attach_id, old_file_path in old_attachments:
            try:
                with transaction.atomic():
                    # Get new rinitialborder_id from mapping
                    new_rinitialborder_id = tarh_mapping.get(rtarh_id)
                    
                    if not new_rinitialborder_id:
                        print(f"  ⚠ Skipping record {old_id}: No mapping for rtarh_id={rtarh_id}")
                        skipped += 1
                        continue
                    
                    # Get new dtyp_attach_id from mapping (if exists)
                    new_dtyp_attach_id = None
                    if dtyp_attach_id:
                        new_dtyp_attach_id = dtarh_attach_mapping.get(dtyp_attach_id)
                    
                    # Prepare file handling - use OLD_MEDIA_ROOT for old files
                    old_file_full_path = os.path.join(OLD_MEDIA_ROOT, old_file_path) if old_file_path else None
                    
                    # Check if old file exists
                    if old_file_path and not os.path.exists(old_file_full_path):
                        print(f"  ⚠ Warning: File not found for record {old_id}: {old_file_full_path}")
                        file_errors += 1
                        # Skip if file doesn't exist
                        skipped += 1
                        continue
                    
                    if not old_file_path:
                        print(f"  ⚠ Skipping record {old_id}: No file path in database")
                        skipped += 1
                        continue
                    
                    # Create new record
                    new_attachment = InitialBorderAttachment(
                        upload_date=upload_date,
                        writed_date=writed_date,
                        rinitialborder_id=new_rinitialborder_id,
                        dtyp_attach_id=new_dtyp_attach_id,
                        writer=None  # Set to None as requested
                    )
                    
                    # Handle file copy from old media location
                    if old_file_path and os.path.exists(old_file_full_path):
                        # Get the filename
                        filename = os.path.basename(old_file_path)
                        
                        # Open the old file from OLD_MEDIA_ROOT and save it to the new record
                        with open(old_file_full_path, 'rb') as f:
                            new_attachment.file.save(filename, File(f), save=False)
                        
                        print(f"  ✓ Transferred file: {old_file_full_path} -> {new_attachment.file.name}")
                    
                    # Save the record
                    new_attachment.save()
                    
                    transferred += 1
                    
                    if transferred % 10 == 0:
                        print(f"  Progress: {transferred}/{total_records} records transferred")
            
            except Exception as e:
                errors += 1
                print(f"  ✗ Error transferring record {old_id}: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"✗ Fatal error during transfer: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        old_cursor.close()
        old_conn.close()
    
    # Final summary
    print("\n" + "=" * 80)
    print("Transfer Complete - Summary")
    print("=" * 80)
    print(f"Total records found:     {total_records}")
    print(f"Successfully transferred: {transferred}")
    print(f"Skipped:                 {skipped}")
    print(f"File not found warnings: {file_errors}")
    print(f"Errors:                  {errors}")
    print("=" * 80)
    
    if transferred > 0:
        print(f"\n✓ Successfully transferred {transferred} TarhAttachment records to InitialBorderAttachment")
        print(f"✓ Files have been copied from {OLD_MEDIA_ROOT} to {new_media_root}")
        print("✓ New files use proper dynamic paths")
    else:
        print("\n⚠ No records were transferred")