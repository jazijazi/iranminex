import psycopg2
import os
import shutil
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password


def transfer_users():
    # Import models
    from accounts.models import User, Company

    try:
        old_conn = psycopg2.connect(
            host='db',
            port=5432,
            database='zarrinold',
            user='zarzar',
            password='Z@r1nAmin913'
        )
        old_conn.autocommit = True
        old_cursor = old_conn.cursor()
        print("✓ Connected to old database (zarrinold)")
    except Exception as e:
        print(f"✗ Failed to connect to old database: {e}")
        return
    

    print("=" * 80)
    print("START USER TRANSFER")
    print("=" * 80)

    DEFAULT_PASSWORD = "NeGarzamin&1382"
    hashed_password = make_password(DEFAULT_PASSWORD)
    
    # Fetch all users from old database
    try:
        old_cursor.execute("""
            SELECT 
                id,
                username,
                first_name,
                last_name,
                first_name_fa,
                last_name_fa,
                address,
                email,
                sherkat_id
            FROM public.permitapi_ipcuser
        """)
        old_users = old_cursor.fetchall()
        print(f"✓ Found {len(old_users)} users in old database")
    except Exception as e:
        print(f"✗ Failed to fetch users from old database: {e}")
        old_cursor.close()
        old_conn.close()
        return

    success_count = 0
    skip_count = 0
    error_count = 0

    for old_user in old_users:
        (
            old_id,
            username,
            first_name,
            last_name,
            first_name_fa,
            last_name_fa,
            address,
            email,
            sherkat_id
        ) = old_user

        try:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                print(f"⊘ Skipped: Username '{username}' already exists")
                skip_count += 1
                continue

            # Find company by sherkat_id if exists
            company = None
            if sherkat_id:
                try:
                    # Get company name and code from old database
                    old_cursor.execute("""
                        SELECT name, code
                        FROM public.prjapi_sherkatejraei
                        WHERE id = %s
                    """, (sherkat_id,))
                    sherkat_data = old_cursor.fetchone()
                    
                    if sherkat_data:
                        sherkat_name, sherkat_code = sherkat_data
                        # Try to find company in new database
                        if sherkat_code:
                            company = Company.objects.filter(name=sherkat_name, code=sherkat_code).first()
                        else:
                            company = Company.objects.filter(name=sherkat_name).first()
                except Exception as e:
                    print(f"  ⚠ Warning: Could not find company for user '{username}': {e}")

            # Create new user
            with transaction.atomic():
                new_user = User(
                    username=username,
                    first_name=first_name or '',
                    last_name=last_name or '',
                    first_name_fa=first_name_fa,
                    last_name_fa=last_name_fa,
                    address=address,
                    password=hashed_password,
                    company=company,
                    is_active=True,
                    is_staff=False,
                    is_superuser=False
                )
                
                # Try to set email, skip if error
                if email:
                    try:
                        new_user.email = email
                    except Exception as e:
                        print(f"  ⚠ Warning: Could not set email for user '{username}': {e}")
                
                new_user.save()
                
                success_count += 1
                company_name = company.name if company else 'N/A'
                print(f"✓ Transferred: {username} (Company: {company_name})")

        except Exception as e:
            error_count += 1
            print(f"✗ Error transferring user '{username}': {e}")
            continue

    # Close connection
    old_cursor.close()
    old_conn.close()

    print("=" * 80)
    print("TRANSFER COMPLETE")
    print(f"✓ Successfully transferred: {success_count}")
    print(f"⊘ Skipped (duplicate): {skip_count}")
    print(f"✗ Errors: {error_count}")
    print(f"Total processed: {len(old_users)}")
    print("=" * 80)
