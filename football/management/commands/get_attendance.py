from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q

class Command(BaseCommand):
    help = 'Получает отфильтрованные записи посещаемости'
    
    def add_arguments(self, parser):
        parser.add_argument('--pressrating', type=float, help='Рейтинг прессы')
        parser.add_argument('--captainrating', type=float, help='Рейтинг капитана')
        parser.add_argument('--coachrating', type=float, help='Рейтинг тренера')
        parser.add_argument('--athleteid_gt', type=int, help='ID атлета больше указанного')
        parser.add_argument('--athleteid_lt', type=int, help='ID атлета меньше указанного')
        parser.add_argument('--rating_gt', type=float, help='Любой рейтинг больше указанного')
        parser.add_argument('--rating_lt', type=float, help='Любой рейтинг меньше указанного')
    
    def handle(self, *args, **options):
        results = self.req_get_attendance(
            pressrating=options['pressrating'],
            captainrating=options['captainrating'],
            coachrating=options['coachrating'],
            athleteid_gt=options['athleteid_gt'],
            athleteid_lt=options['athleteid_lt'],
            rating_gt=options['rating_gt'],
            rating_lt=options['rating_lt']
        )