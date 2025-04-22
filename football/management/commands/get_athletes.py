from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Получает отфильтрованных атлетов из базы данных'
    
    def add_arguments(self, parser):
        parser.add_argument('--dateofbirth__year__gt', type=int, help='Год рождения больше указанного')
        parser.add_argument('--weight', type=float, help='Точный вес атлета')
        parser.add_argument('--height', type=float, help='Точный рост атлета')
        # parser.add_argument('--athleteid_gt', type=int, help='ID атлета больше указанного')
    
    def handle(self, *args, **options):
        results = self.req_get_athletes(
            year_gt=options['dateofbirth__year__gt'],
            weight=options['weight'],
            height=options['height'],
            # athleteid_gt=options['athleteid_gt']
        )
        