from django.core.management.base import BaseCommand
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json

class Command(BaseCommand):
    help = 'Получает отфильтрованные данные о командах'
    
    def add_arguments(self, parser):
        parser.add_argument('--wins', type=int, help='Точное количество побед')
        parser.add_argument('--losses', type=int, help='Точное количество поражений')
        parser.add_argument('--wins_gt', type=int, help='Побед больше указанного числа')
        parser.add_argument('--losses_lt', type=int, help='Поражений меньше указанного числа')
        parser.add_argument('--output', type=str, help='Файл для вывода результатов (json)')
    
    def handle(self, *args, **options):
        results = self.req_get_teams(
            wins=options['wins'],
            losses=options['losses'],
            wins_gt=options['wins_gt'],
            losses_lt=options['losses_lt']
        )
        
        if options['output']:
            with open(options['output'], 'w') as f:
                json.dump(results, f, indent=2, cls=DjangoJSONEncoder)
            self.stdout.write(self.style.SUCCESS(f"Данные сохранены в {options['output']}"))
        else:
            self.print_results(results)