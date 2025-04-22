from django.core.management.base import BaseCommand
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json

class Command(BaseCommand):
    help = 'Получает отфильтрованные данные о турнирах'
    
    def add_arguments(self, parser):
        parser.add_argument('--startdate_year_gt', type=int, help='Год начала турнира больше указанного')
        parser.add_argument('--rating', type=float, help='Точный рейтинг турнира')
        parser.add_argument('--rating_gt', type=float, help='Рейтинг больше указанного')
        parser.add_argument('--rating_lt', type=float, help='Рейтинг меньше указанного')
        parser.add_argument('--output', type=str, help='Файл для вывода результатов (json)')
    
    def handle(self, *args, **options):
        results = self.req_get_tournaments(
            startdate_year_gt=options['startdate_year_gt'],
            rating=options['rating'],
            rating_gt=options['rating_gt'],
            rating_lt=options['rating_lt']
        )
        
        if options['output']:
            with open(options['output'], 'w') as f:
                json.dump(results, f, indent=2, cls=DjangoJSONEncoder)
            self.stdout.write(self.style.SUCCESS(f"Данные сохранены в {options['output']}"))
        else:
            self.print_results(results)