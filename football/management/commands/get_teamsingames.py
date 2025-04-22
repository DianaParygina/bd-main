from django.core.management.base import BaseCommand
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json

class Command(BaseCommand):
    help = 'Получает первые 100 записей о командах в играх'
    
    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=100, 
                          help='Количество записей (по умолчанию: 100)')
        parser.add_argument('--output', type=str, 
                          help='Файл для вывода результатов')
    
    def handle(self, *args, **options):
        results = self.req_get_teamsingames(
            limit=options['limit']
        )
        
        if options['output']:
            with open(options['output'], 'w') as f:
                json.dump(results, f, indent=2, cls=DjangoJSONEncoder)
            self.stdout.write(self.style.SUCCESS(f"Данные сохранены в {options['output']}"))
        else:
            self.print_results(results)