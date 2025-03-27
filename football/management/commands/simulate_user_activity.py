import random
import time
import threading
from datetime import datetime, timedelta
from django.db import connection, transaction
from faker import Faker
from django.db.models import Count, Avg, Q, F
from django.core.management.base import BaseCommand
from football.models import (
    Applications, Athletes, Attendance, Coaches, Games, Results, Teams, Teamsingames, Tournaments, Trainings
)

fake = Faker(['ru_RU'])

class DatabaseUser:
    def __init__(self, username):
        self.username = username

    def execute_query(self, query, params=None):
        with connection.cursor() as cursor:
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if query.lower().startswith('select'):
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount

                print(f"{self.username}: {query[:50]}... {'Успешно' if result else 'Нет данных'}")
                return result

            except Exception as e:
                print(f"{self.username}: {query[:50]}... Ошибка: {e}")
                return None


def generate_queries(user):
    queries = {
        'create': [
            (
                "INSERT INTO football_tournaments (name, location, startdate, enddate, rating) VALUES (%s, %s, %s, %s, %s)",
                lambda: (
                    fake.word().capitalize() + " Турнир",
                    fake.city(),
                    fake.date_time_between(start_date='-30y', end_date='now'),
                    fake.date_time_between(start_date='-30y', end_date='now'),
                    random.randint(1, 100),
                )
            ),
            (
                "INSERT INTO football_coaches (fullname, dateofbirth) VALUES (%s, %s)",
                lambda: (fake.name(), fake.date_time_between(start_date='-70y', end_date='-30y'))
            ),
            (
                "INSERT INTO football_athletes (fullname, dateofbirth, weight, height, gender) VALUES (%s, %s, %s, %s, %s)",
                lambda: (
                    fake.name(),
                    fake.date_time_between(start_date='-40y', end_date='-18y'),
                    round(random.uniform(50, 100), 2),
                    random.randint(150, 200),
                    random.choice(['Male', 'Female'])
                )
            ),
            (
                "INSERT INTO football_teams (coachid_id, name, rating, wins, losses, draws) VALUES (%s, %s, %s, %s, %s, %s)",
                lambda: (
                    random.choice(Coaches.objects.values_list('coachid', flat=True) or [None]),
                    fake.company(),
                    random.randint(1, 100),
                    random.randint(0, 50),
                    random.randint(0, 50),
                    random.randint(0, 50)
                )
            ),
            (
                "INSERT INTO football_applications (tournamentid_id, status) VALUES (%s, %s)",
                lambda: (
                    random.choice(Tournaments.objects.values_list('tournamentid', flat=True) or [None]),
                    random.choice(['Pending', 'Approved', 'Rejected'])
                )
            ),
            (
                "INSERT INTO football_games (tournamentid_id, date, location, score, hierarchy) VALUES (%s, %s, %s, %s, %s)",
                lambda: (
                    random.choice(Tournaments.objects.values_list('tournamentid', flat=True) or [None]),
                    fake.date_time_between(start_date='-30y', end_date='now'),
                    fake.city(),
                    f"{random.randint(0, 5)}-{random.randint(0, 5)}",
                    random.randint(1, 10),
                )
            ),
             (
                "INSERT INTO football_teamsingames (teamid_id, gameid_id) VALUES (%s, %s)",
                lambda: (
                    random.choice(Teams.objects.values_list('teamid', flat=True) or [None]),
                    random.choice(Games.objects.values_list('gameid', flat=True) or [None])
                )
            ),       
            (
                "INSERT INTO football_results (athleteid_id, athleteplace, goalsscored) VALUES (%s, %s, %s)",
                lambda: (
                    random.choice(Athletes.objects.values_list('athleteid', flat=True) or [None]),
                    random.randint(1, 10),
                    random.randint(0,5)
                )
            ),
            (
                "INSERT INTO football_trainings (teamid_id, name, date) VALUES (%s, %s, %s)",
                lambda: (
                    random.choice(Teams.objects.values_list('teamid', flat=True) or [None]),
                    fake.word().capitalize() + " Тренировка",
                    fake.date_time_between(start_date='-30y', end_date='now')
                )
            ),
            (
                "INSERT INTO football_attendance (athleteid_id, pressrating, captainrating, coachrating) VALUES (%s, %s, %s, %s)",
                lambda: (
                    random.choice(Athletes.objects.values_list('athleteid', flat=True) or [None]),
                    random.randint(1,10),
                    random.randint(1,10),
                    random.randint(1,10)

                )
            ),                                                
        ],

        'read': [
            ("SELECT * FROM football_athletes WHERE athleteid = %s", lambda: (random.randint(1, Athletes.objects.count() or 1),)),
            ("SELECT fullname, dateofbirth FROM football_coaches WHERE coachid = %s", lambda: (random.randint(1, Coaches.objects.count() or 1),)),
            ("SELECT name FROM football_teams WHERE coachid_id = %s", lambda: (random.randint(1, Coaches.objects.count() or 1),)),
            ("SELECT * FROM football_tournaments WHERE startdate BETWEEN %s AND %s", lambda: (datetime.now() - timedelta(days=365*10), datetime.now())), # Исправлено

            ("SELECT status FROM football_applications WHERE tournamentid_id = %s", lambda: (random.randint(1, Tournaments.objects.count() or 1),)),
            ("SELECT location, score FROM football_games WHERE tournamentid_id = %s", lambda: (random.randint(1, Tournaments.objects.count() or 1),)),
            ("SELECT date FROM football_trainings WHERE teamid_id = %s", lambda: (random.randint(1, Teams.objects.count() or 1),)),
            ("SELECT COUNT(*) FROM football_athletes WHERE gender = 'Male'", None), # Здесь None, так как нет параметров
            ("SELECT AVG(rating) FROM football_teams", None), # Здесь None, так как нет параметров
            ("SELECT T.name FROM football_tournaments T JOIN football_games G ON T.tournamentid = G.tournamentid_id WHERE G.date > %s", lambda: (datetime.now() - timedelta(days=365*5),)),
            ("SELECT fullname FROM football_athletes WHERE height > 180 AND weight < 80", None), # Здесь None, так как нет параметров
            ("SELECT * FROM football_teamsingames WHERE teamid_id = %s", lambda: (random.randint(1, Teams.objects.count() or 1),)),
            ("SELECT * FROM football_results WHERE athleteid_id = %s", lambda: (random.randint(1, Athletes.objects.count() or 1),)),
            ("SELECT * FROM football_attendance WHERE athleteid_id = %s", lambda: (random.randint(1, Athletes.objects.count() or 1),)),

        ],

        'update': [ #исправлены все запросы на обновление
            ("UPDATE football_teams SET rating = %s WHERE teamid = %s", lambda: (random.randint(1, 100), random.randint(1, Teams.objects.count() or 1))),
            ("UPDATE football_athletes SET weight = weight + %s WHERE athleteid = %s", lambda: (random.uniform(-5, 5), random.randint(1, Athletes.objects.count() or 1))),
            ("UPDATE football_tournaments SET rating = rating + %s WHERE tournamentid = %s AND rating < 90", lambda: (random.randint(1, 10), random.randint(1, Tournaments.objects.count() or 1))),
            ("UPDATE football_games SET score = %s WHERE gameid = %s and date < %s", lambda: (f"{random.randint(0, 5)}-{random.randint(0, 5)}", random.randint(1, Games.objects.count() or 1), datetime.now())),
            ("UPDATE football_coaches SET fullname = %s WHERE coachid = %s", lambda: (fake.name(), random.randint(1, Coaches.objects.count() or 1))),
            ("UPDATE football_applications SET status = %s WHERE applicationid = %s", lambda: (random.choice(['Pending', 'Approved', 'Rejected']), random.randint(1, Applications.objects.count() or 1))),
            ("UPDATE football_results SET goalsscored = %s WHERE resultid = %s", lambda: (random.randint(0, 10), random.randint(1, Results.objects.count() or 1))),
            ("UPDATE football_trainings SET name = %s WHERE trainingid = %s", lambda: (fake.word().capitalize() + " Тренировка", random.randint(1, Trainings.objects.count() or 1))),
            ("UPDATE football_attendance SET pressrating = %s WHERE attendanceid = %s", lambda: (random.randint(1, 10), random.randint(1, Attendance.objects.count() or 1))),
            ("UPDATE football_teamsingames SET gameid_id = %s WHERE teamsingameid = %s", lambda: (random.choice(Games.objects.values_list('gameid', flat=True) or [None]), random.randint(1, Teamsingames.objects.count() or 1)))
        ],
        'delete': [ #исправлены все запросы на удаление
            ("DELETE FROM football_applications WHERE applicationid = %s", lambda: (random.randint(1, Applications.objects.count() or 1),)),
            ("DELETE FROM football_results WHERE resultid = %s", lambda: (random.randint(1, Results.objects.count() or 1),)),
            ("DELETE FROM football_trainings WHERE trainingid = %s", lambda: (random.randint(1, Trainings.objects.count() or 1),)),
            ("DELETE FROM football_attendance WHERE attendanceid = %s", lambda: (random.randint(1, Attendance.objects.count() or 1),)),
            ("DELETE FROM football_teamsingames WHERE teamsingameid = %s", lambda: (random.randint(1, Teamsingames.objects.count() or 1),)),


        ],
    }

    operation = random.choices(['read', 'create', 'update', 'delete'], weights=[0.7, 0.15, 0.1, 0.05])[0]
    query_template, param_generator = random.choice(queries[operation])
    params = param_generator() if callable(param_generator) else param_generator
    return query_template, params


def simulate_user_activity(username):

    user = DatabaseUser(username)
    while True:
        query, params = generate_queries(user)
        with transaction.atomic():
            user.execute_query(query, params)
        time.sleep(random.uniform(0.1, 2))


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