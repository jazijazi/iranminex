import json
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from accounts.models import User, Roles
from common.models import Company


class Command(BaseCommand):
    help = 'Transfer old IpcUser data to new User model'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to the JSON file containing old IpcUser data'
        )

    def load_json(self, file_path):
        """Load and parse JSON file, skipping any preamble"""
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            json_start = content.find('[')
            if json_start == -1:
                self.stdout.write(self.style.ERROR(f'No JSON array found in {file_path}'))
                return None
            
            if json_start > 0:
                content = content[json_start:]
            
            return json.loads(content)

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        data = self.load_json(json_file)
        if not data:
            return
        
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(data)} users from {json_file}'))
        
        # Statistics
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        # Default password hash
        default_password = make_password("New#33#gis")
        
        for item in data:
            try:
                fields = item['fields']
                old_pk = item['pk']
                
                username = fields.get('username', '')
                
                # Check if username is too long for new model (max 25 chars)
                if len(username) > 25:
                    self.stdout.write(
                        self.style.WARNING(f"Skipping user {username}: username too long ({len(username)} chars)")
                    )
                    skipped_count += 1
                    continue
                
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    self.stdout.write(
                        self.style.WARNING(f"Skipping user {username}: already exists")
                    )
                    skipped_count += 1
                    continue
                
                # Get Roles FK
                roles_instance = None
                if fields.get('roles'):
                    try:
                        roles_instance = Roles.objects.get(pk=fields['roles'])
                    except Roles.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Roles with pk {fields['roles']} not found for user {username}")
                        )
                
                # Get Company FK (was sherkat)
                company_instance = None
                if fields.get('sherkat'):
                    try:
                        company_instance = Company.objects.get(pk=fields['sherkat'])
                    except Company.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f"Company with pk {fields['sherkat']} not found for user {username}")
                        )
                
                # Create new User
                new_user = User.objects.create(
                    username=username,
                    first_name=fields.get('first_name', ''),
                    last_name=fields.get('last_name', ''),
                    email=fields.get('email', ''),
                    password=default_password,  # Use default password
                    first_name_fa=fields.get('first_name_fa'),
                    last_name_fa=fields.get('last_name_fa'),
                    address=fields.get('address'),
                    roles=roles_instance,
                    company=company_instance,
                    is_active=fields.get('is_active', True),
                    is_staff=fields.get('is_staff', False),
                    is_superuser=fields.get('is_superuser', False),
                    date_joined=fields.get('date_joined'),
                )
                
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f"Created User: {new_user.username} (old pk: {old_pk})")
                )
                
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"Error processing user {item.get('pk')}: {str(e)}")
                )
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Transfer Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Skipped: {skipped_count}'))
        self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))
        self.stdout.write(self.style.SUCCESS(f'\nDefault password for all users: New#33#gis'))