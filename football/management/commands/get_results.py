from django.core.management.base import BaseCommand
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json

class Command(BaseCommand):
    help = 'Получает отфильтрованные результаты из базы данных'
    
    def add_arguments(self, parser):
        parser.add_argument('--athleteplace', type=int, help='Место атлета')
        parser.add_argument('--goalsscored', type=int, help='Количество забитых голов')
        # parser.add_argument('--athleteid_lt', type=int, help='ID атлета меньше указанного')
        parser.add_argument('--output', type=str, help='Файл для вывода результатов (json)')
    
    def handle(self, *args, **options):
        results = self.req_get_results(
            athleteplace=options['athleteplace'],
            goalsscored=options['goalsscored'],
            # athleteid_lt=options['athleteid_lt']
        )
        
        if options['output']:
            with open(options['output'], 'w') as f:
                json.dump(results, f, indent=2, cls=DjangoJSONEncoder)
            self.stdout.write(self.style.SUCCESS(f"Данные сохранены в {options['output']}"))
        else:
            self.print_results(results)