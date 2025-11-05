import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Импорт телефонов из CSV файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            dest='file',
            default='phones.csv',
            help='CSV file to import (default: phones.csv)',
        )

    def handle(self, *args, **options):
        file_path = options['file']
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                phone_id = int(row['id'])
                name = row['name']
                image = row['image']
                price = float(row['price'])
                release_date = row['release_date']
                lte_exists = row['lte_exists'].strip().lower() == 'true'
                slug = slugify(name)

                obj, created = Phone.objects.update_or_create(
                    id=phone_id,
                    defaults={
                        'name': name,
                        'image': image,
                        'price': price,
                        'release_date': release_date,
                        'lte_exists': lte_exists,
                        'slug': slug,
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Added: {name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Updated: {name}'))
        self.stdout.write(self.style.SUCCESS('Import finished.'))
