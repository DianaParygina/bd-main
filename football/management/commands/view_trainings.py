from django.core.management.base import BaseCommand
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json

class Command(BaseCommand):
    help = 'Получает отфильтрованные данные о тренировках из view_trainings'
    
    def add_arguments(self, parser):
        parser.add_argument('--date_year_gt', type=int, help='Год тренировки больше указанного')
        parser.add_argument('--date_year_lt', type=int, help='Год тренировки меньше указанного')
        parser.add_argument('--date_exact', type=str, help='Точная дата тренировки (YYYY-MM-DD)')
        parser.add_argument('--output', type=str, help='Файл для вывода результатов (json)')
    
    def handle(self, *args, **options):
        results = self.req_get_trainings(
            date_year_gt=options['date_year_gt'],
            date_year_lt=options['date_year_lt'],
            date_exact=options['date_exact']
        )
        
        if options['output']:
            with open(options['output'], 'w') as f:
                json.dump(results, f, indent=2, cls=DjangoJSONEncoder)
            self.stdout.write(self.style.SUCCESS(f"Данные сохранены в {options['output']}"))
        else:
            self.print_results(results)