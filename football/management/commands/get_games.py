from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Получает отфильтрованные игры из базы данных'
    
    def add_arguments(self, parser):
        parser.add_argument('--year_gt', type=int, help='Год проведения больше указанного')
        parser.add_argument('--year_lt', type=int, help='Год проведения меньше указанного')
        parser.add_argument('--score', type=str, help='Точный счет игры')
        parser.add_argument('--score_contains', type=str, help='Часть счета игры')
        parser.add_argument('--hierarchy', type=int, help='Уровень важности игры')
        parser.add_argument('--tournamentid_gt', type=int, help='ID турнира больше указанного')
    
    def handle(self, *args, **options):
        results = self.req_get_games(
            year_gt=options['year_gt'],
            year_lt=options['year_lt'],
            score=options['score'],
            score_contains=options['score_contains'],
            hierarchy=options['hierarchy'],
            tournamentid_gt=options['tournamentid_gt']
        )