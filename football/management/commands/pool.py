import random
import time
import threading
from datetime import datetime, timedelta
from django.db import connection
from faker import Faker
from django.db.models import Count, Avg, Q
from django.core.management.base import BaseCommand
from football.models import (
    Applications, Athletes, Attendance, Coaches, Games, Results, Teams, Teamsingames, Tournaments, Trainings
)

fake = Faker(['ru_RU'])

class DatabaseUser:
    def __init__(self, username):
        self.username = username

    def execute_query(self, query, params=None):
        try:
            with connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall() if query.lower().startswith('select') else cursor.rowcount
                print(f"{self.username}: {query[:50]}... {'Успешно' if result else 'Нет данных'}")
                return result
        except Exception as e:
            print(f"{self.username}: {query[:50]}... Ошибка: {e}")
            return None
        finally:
            connection.close()


def generate_queries(user):
    queries = {
        'create': [
    ("INSERT INTO [Tournaments] ([Name], [Location], [StartDate], [EndDate], [Rating]) VALUES (%s, %s, %s, %s, %s)", (fake.word().capitalize() + " Турнир", fake.city(), fake.date_time_between(start_date='-30y', end_date='now'), fake.date_time_between(start_date='-30y', end_date='now'), random.randint(1, 100))),
    ("INSERT INTO [Coaches] ([FullName], [DateOfBirth]) VALUES (%s, %s)", (fake.name(), fake.date_time_between(start_date='-70y', end_date='-30y'))),
    ("INSERT INTO [Athletes] ([FullName], [DateOfBirth], [Weight], [Height], [Gender]) VALUES (%s, %s, %s, %s, %s)", (fake.name(), fake.date_time_between(start_date='-40y', end_date='-18y'), random.uniform(50, 100), random.randint(150, 200), random.choice(['Male', 'Female']))),
    ("INSERT INTO [Teams] ([CoachID], [Name], [Rating], [Wins], [Losses], [Draws]) VALUES (%s, %s, %s, %s, %s, %s)", (random.choice(Coaches.objects.values_list('coachid', flat=True)), fake.company(), random.randint(1, 100), random.randint(0, 50), random.randint(0, 50), random.randint(0, 50))),
    ("INSERT INTO [Games] ([TournamentID], [Date], [Location], [Score], [Hierarchy]) VALUES (%s, %s, %s, %s, %s)", (random.choice(Tournaments.objects.values_list('tournamentid', flat=True)), fake.date_time_between(start_date='-30y', end_date='now'), fake.city(), f"{random.randint(0, 5)}-{random.randint(0, 5)}", random.randint(1, 10))),
    ("INSERT INTO [TeamsInGames] ([TeamID], [GameID]) VALUES (%s, %s)", (random.choice(Teams.objects.values_list('teamid', flat=True)), random.choice(Games.objects.values_list('gameid', flat=True)))),
],

'read': [
    ("SELECT * FROM [Athletes] WHERE AthleteID = %s", (random.choice(Athletes.objects.values_list('athleteid', flat=True)) or 1,)),  # Athletes
    ("SELECT * FROM [Coaches] WHERE CoachID = %s", (random.choice(Coaches.objects.values_list('coachid', flat=True)) or 1,)),  # Coaches
    ("SELECT * FROM [Teams] WHERE CoachID = %s", (random.choice(Coaches.objects.values_list('coachid', flat=True)) or 1,)),  # Teams
    ("SELECT * FROM [Tournaments] WHERE StartDate BETWEEN %s AND %s", (datetime.now() - timedelta(days=365*10), datetime.now())),  # Tournaments

    ("SELECT * FROM [Applications] WHERE TournamentID = %s", (random.choice(Tournaments.objects.values_list('tournamentid', flat=True)) or 1,)),
    ("SELECT * FROM [Games] WHERE TournamentID = %s", (random.choice(Tournaments.objects.values_list('tournamentid', flat=True)) or 1,)),  # Games
    ("SELECT * FROM [Trainings] WHERE TeamID = %s", (random.choice(Teams.objects.values_list('teamid', flat=True)) or 1,)),  # Trainings
],

'update': [
    ("UPDATE [Teams] SET Rating = %s WHERE TeamID = %s", (random.randint(1, 100), random.choice(Teams.objects.values_list('teamid', flat=True)) or 1)),
    ("UPDATE [Athletes] SET Weight = %s WHERE AthleteID = %s", (random.uniform(50, 100), random.choice(Athletes.objects.values_list('athleteid', flat=True)) or 1)),
    ("UPDATE [Coaches] SET FullName = %s WHERE CoachID = %s", (fake.name(), random.choice(Coaches.objects.values_list('coachid', flat=True)) or 1)),
    ("UPDATE [Tournaments] SET Rating = %s WHERE TournamentID = %s", (random.randint(1, 100), random.choice(Tournaments.objects.values_list('tournamentid', flat=True)) or 1)),

    ("UPDATE [Games] SET Score = %s WHERE GameID = %s", (f"{random.randint(0, 5)}-{random.randint(0, 5)}", random.choice(Games.objects.values_list('gameid', flat=True)) or 1)),
],

'delete': [
    ("DELETE FROM [Applications] WHERE ApplicationID = %s", (random.choice(Applications.objects.values_list('applicationid', flat=True)) or 1,)), 
    ("DELETE FROM [Results] WHERE ResultID = %s", (random.choice(Results.objects.values_list('resultid', flat=True)) or 1,)),
    ("DELETE FROM [TeamsInGames] WHERE TeamsingameID = %s", (random.choice(Teamsingames.objects.values_list('teamsingameid', flat=True)) or 1,)),
    ("DELETE FROM [Trainings] WHERE TrainingID = %s", (random.choice(Trainings.objects.values_list('trainingid', flat=True)) or 1,)),
],
    }

    operation = random.choices(['read', 'create', 'update', 'delete'], weights=[0.7, 0.2, 0.08, 0.02])[0] 
    query, params = random.choice(queries[operation])
    return query, params




def simulate_user_activity(username):
    user = DatabaseUser(username)
    while True:
        query, params = generate_queries(user)
        user.execute_query(query, params)
        time.sleep(random.uniform(0.1, 2))  


if __name__ == "__main__":
    usernames = [fake.user_name() for _ in range(20)]  
    threads = []
    for username in usernames:
        thread = threading.Thread(target=simulate_user_activity, args=(username,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()



class Command(BaseCommand):
    help = 'Simulates user activity with the database'

    def handle(self, *args, **options):
        usernames = [fake.user_name() for _ in range(20)]
        threads = []
        for username in usernames:
            thread = threading.Thread(target=simulate_user_activity, args=(username,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()  
