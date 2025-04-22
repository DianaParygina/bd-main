from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Получает отфильтрованных тренеров из базы данных'
    
    def add_arguments(self, parser):
        parser.add_argument('--name_contains', type=str, help='Часть имени тренера')
        parser.add_argument('--year_lt', type=int, help='Год рождения меньше указанного')
        parser.add_argument('--coachid_gt', type=int, help='ID тренера больше указанного')
    
    def handle(self, *args, **options):
        results = self.req_get_coaches(
            name_contains=options['name_contains'],
            year_lt=options['year_lt'],
            coachid_gt=options['coachid_gt']
        )