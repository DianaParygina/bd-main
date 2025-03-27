from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta
from django.db.utils import IntegrityError
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP

from football.models import (
    Applications, Athletes, Attendance, Coaches, Games, Results, Teams, Teamsingames, Tournaments, Trainings
)

fake = Faker(['ru_RU'])

class Command(BaseCommand):
    help = 'Генерация реалистичных данных для базы данных'

    def handle(self, *args, **options):
        self.generate_tournaments(10000)
        self.generate_coaches(5000)
        self.generate_teams(20000)
        self.generate_athletes(100000)
        self.generate_applications(50000)
        self.generate_games(100000)
        self.generate_teams_in_games(200000)
        self.generate_results(500000)
        self.generate_trainings(100000)
        self.generate_attendance(500000)

    def generate_tournaments(self, count):
        for _ in range(count):
            start_date = fake.date_time_between(start_date='-30y', end_date='now', tzinfo=timezone.get_current_timezone())
            end_date = start_date + timedelta(days=random.randint(1, 14))

            Tournaments.objects.create(
                name=fake.word().capitalize() + " Турнир",
                location=fake.city(),
                startdate=start_date,
                enddate=end_date,
                rating=random.randint(1, 100)
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} турниров'))

    def generate_coaches(self, count):
        for _ in range(count):
            Coaches.objects.create(
                fullname=fake.name(),
                dateofbirth=fake.date_time_between(start_date='-70y', end_date='-30y', tzinfo=timezone.get_current_timezone())
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} тренеров'))

    def generate_teams(self, count):
        coaches = list(Coaches.objects.all())
        for _ in range(count):
            Teams.objects.create(
                coachid=random.choice(coaches),
                name=fake.word().capitalize() + " Команда",
                rating=random.randint(1, 100),
                wins=random.randint(0, 100),
                losses=random.randint(0, 100),
                draws=random.randint(0, 100)
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} команд'))

    def generate_athletes(self, count):
        for _ in range(count):
            weight = round(random.uniform(0, 99.99), 2)
            Athletes.objects.create(
                fullname=fake.name(),
                dateofbirth=fake.date_time_between(start_date='-40y', end_date='-18y', tzinfo=timezone.get_current_timezone()),
                weight = weight,  
                height=random.randint(150, 200),
                gender=random.choice(['Male', 'Female'])
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} спортсменов'))

    def generate_applications(self, count):
        tournaments = list(Tournaments.objects.all())
        statuses = ['Pending', 'Approved', 'Rejected']
        for _ in range(count):
            Applications.objects.create(
                tournamentid=random.choice(tournaments),
                status=random.choice(statuses)
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} заявок'))

    def generate_games(self, count):
        tournaments = list(Tournaments.objects.all())
        for _ in range(count):
            Games.objects.create(
                tournamentid=random.choice(tournaments),
                date=fake.date_time_between(start_date='-30y', end_date='now', tzinfo=timezone.get_current_timezone()),
                location=fake.city(),
                score=f"{random.randint(0, 5)}-{random.randint(0, 5)}",
                hierarchy=random.randint(1, 10)
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} игр'))

    def generate_teams_in_games(self, count):
        teams = list(Teams.objects.all())
        games = list(Games.objects.all())
        for _ in range(count):
            try:
                Teamsingames.objects.create(
                    teamid=random.choice(teams),
                    gameid=random.choice(games)
                )
            except IntegrityError:
                pass
        self.stdout.write(self.style.SUCCESS(f'Создано (или попытка создать) {count} связей команд и игр'))

    def generate_results(self, count):
        athletes = list(Athletes.objects.all())
        for _ in range(count):
            Results.objects.create(
                athleteid=random.choice(athletes),
                athleteplace=random.randint(1, 100),
                goalsscored=random.randint(0, 10)
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} результатов'))

    def generate_trainings(self, count):
        teams = list(Teams.objects.all())
        for _ in range(count):
            Trainings.objects.create(
                teamid=random.choice(teams),
                name=fake.word().capitalize() + " Тренировка",
                date=fake.date_time_between(start_date='-30y', end_date='now', tzinfo=timezone.get_current_timezone())
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} тренировок'))

    def generate_attendance(self, count):
        athletes = list(Athletes.objects.all())
        for _ in range(count):
            Attendance.objects.create(
                athleteid=random.choice(athletes),
                pressrating=random.randint(1, 10),
                captainrating=random.randint(1, 10),
                coachrating=random.randint(1, 10)
            )
        self.stdout.write(self.style.SUCCESS(f'Создано {count} записей посещаемости'))