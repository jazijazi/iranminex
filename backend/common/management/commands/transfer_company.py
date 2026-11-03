import json
import os
from django.core.management.base import BaseCommand
from common.models import Company


class Command(BaseCommand):
    help = 'Transfer old SherkatEjraei data to new Company model'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help='Path to the JSON file containing old SherkatEjraei data'
        )

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        if not os.path.exists(json_file):
            self.stdout.write(self.style.ERROR(f'File not found: {json_file}'))
            return
        
        # Check file size
        file_size = os.path.getsize(json_file)
        if file_size == 0:
            self.stdout.write(self.style.ERROR(f'File is empty: {json_file}'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'File size: {file_size} bytes'))
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    self.stdout.write(self.style.ERROR('File content is empty'))
                    return
                
                # Find the first '[' character to skip any preamble
                json_start = content.find('[')
                if json_start == -1:
                    self.stdout.write(self.style.ERROR('No JSON array found in file'))
                    return
                
                if json_start > 0:
                    self.stdout.write(self.style.WARNING(f'Skipping {json_start} characters of preamble'))
                    content = content[json_start:]
                
                data = json.loads(content)
                
        except UnicodeDecodeError:
            self.stdout.write(self.style.WARNING('UTF-8 failed, trying latin-1...'))
            with open(json_file, 'r', encoding='latin-1') as f:
                content = f.read()
                json_start = content.find('[')
                if json_start > 0:
                    content = content[json_start:]
                data = json.loads(content)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'JSON decode error: {str(e)}'))
            return
        
        if not isinstance(data, list):
            self.stdout.write(self.style.ERROR('JSON root must be a list'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(data)} records from {json_file}'))
        
        # Track statistics
        created_count = 0
        error_count = 0
        
        for item in data:
            try:
                fields = item['fields']
                old_pk = item['pk']
                
                # Create new Company - fields are identical
                new_instance = Company.objects.create(
                    name=fields.get('name', ''),
                    code=fields.get('code'),
                    typ=fields.get('typ'),
                    service_typ=fields.get('service_typ'),
                    callnumber=fields.get('callnumber'),
                    address=fields.get('address'),
                    comment=fields.get('comment')
                )
                
                created_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f"Created Company: {new_instance.name} (old pk: {old_pk})")
                )
                
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"Error processing record {item.get('pk')}: {str(e)}")
                )
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Transfer Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
        self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))