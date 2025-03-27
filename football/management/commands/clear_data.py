from django.core.management.base import BaseCommand
from football.models import (
    Applications, Athletes, Attendance, Coaches, Games, Results, Teams, Teamsingames, Tournaments, Trainings
)

class Command(BaseCommand):
    help = 'Удаление всех данных из таблиц'

    def handle(self, *args, **options):
        # Удаление данных из всех таблиц
        Applications.objects.all().delete()
        Athletes.objects.all().delete()
        Attendance.objects.all().delete()
        Coaches.objects.all().delete()
        Games.objects.all().delete()
        Results.objects.all().delete()
        Teams.objects.all().delete()
        Teamsingames.objects.all().delete()
        Tournaments.objects.all().delete()
        Trainings.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Все данные успешно удалены из таблиц'))