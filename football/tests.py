from django.test import TestCase
from .models import Applications, Athletes, Attendance, Coaches, Games, Results, Teams, Teamsingames, Tournaments, Trainings 
from rest_framework.test import APIClient
from model_bakery import baker
from datetime import datetime, timezone


class CoachesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_coaches(self):
        coach = baker.make("football.Coaches")

        r = self.client.get('/api/coaches/')
        data = r.json()
        print(data)

        assert coach.fullname == data[0]['fullname']
        assert coach.coachid == data[0]['coachid']
        assert coach.dateofbirth == data[0]['dateofbirth'] # даты сравниваем как строки
        assert len(data) == 1


    def test_create_coach(self):
        r = self.client.post("/api/coaches/", {
            "fullname": "Test Coach",
            "dateofbirth": "1980-01-01T00:00:00Z", 
        })

        new_coaches_id = r.json()['coachid']

        coaches = Coaches.objects.all()
        assert len(coaches) == 1

        new_coach = Coaches.objects.filter(coachid=new_coaches_id).first()
        assert new_coach.fullname == "Test Coach"
        assert new_coach.dateofbirth == datetime(1980, 1, 1, tzinfo=timezone.utc)


    def test_delete_coach(self):
        coaches = baker.make("football.Coaches", 10)
        r = self.client.get('/api/coaches/')
        data = r.json()
        assert len(data) == 10

        coaches_id_to_delete = coaches[3].coachid
        self.client.delete(f'/api/coaches/{coaches_id_to_delete}/')

        r = self.client.get('/api/coaches/')
        data = r.json()
        assert len(data) == 9

        assert coaches_id_to_delete not in [i['coachid'] for i in data]
        

    def test_update_coach(self):
        coaches = baker.make("football.Coaches", 10)
        coache: Coaches = coaches[2]

        r = self.client.get(f'/api/coaches/{coache.coachid}/')
        data = r.json()
        assert data['fullname'] == coache.fullname

        r = self.client.put(f'/api/coaches/{coache.coachid}/', {
            "fullname": "Вася Иванов"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/coaches/{coache.coachid}/')
        data = r.json()
        assert data['fullname'] == "Вася Иванов"

        coache.refresh_from_db()
        assert data['fullname'] == coache.fullname       

    

class TeamsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_teams(self):
        coach = baker.make("football.Coaches") # Create a related coach
        team = baker.make("football.Teams", coachid=coach)  # Use related coach

        r = self.client.get('/api/teams/')
        data = r.json()
        print(data)

        assert team.name == data[0]['name']
        assert team.teamid == data[0]['teamid']
        assert team.coachid.coachid == data[0]['coachid']  # Access coachid through the relationship
        assert team.rating == data[0]['rating']
        assert team.wins == data[0]['wins']
        assert team.losses == data[0]['losses']
        assert team.draws == data[0]['draws']
        assert len(data) == 1

    def test_create_team(self):
        coach = baker.make("football.Coaches") # Create the coach first
        r = self.client.post("/api/teams/", {
            "coachid": coach.coachid,  # Use the coach's coachid
            "name": "Test Team",
            "rating": 100,
            "wins": 5,
            "losses": 2,
            "draws": 3,
        })
        data = r.json()
        print(r.json())

        new_teams_id = r.json()['teamid']

        teams = Teams.objects.all()
        assert len(teams) == 1

        new_team = Teams.objects.filter(teamid=new_teams_id).first()
        assert new_team.name == "Test Team"
        assert new_team.coachid.coachid == coach.coachid # Compare coachid, not the whole coach object
        assert new_team.rating == 100
        assert new_team.wins == 5
        assert new_team.losses == 2
        assert new_team.draws == 3
        


    def test_delete_team(self):
        coach = baker.make("football.Coaches") # coach needed for related field
        teams = baker.make("football.Teams", 10, coachid=coach)  # Create teams with related coach
        r = self.client.get('/api/teams/')
        data = r.json()
        assert len(data) == 10

        teams_id_to_delete = teams[3].teamid
        self.client.delete(f'/api/teams/{teams_id_to_delete}/')

        r = self.client.get('/api/teams/')
        data = r.json()
        assert len(data) == 9

        assert teams_id_to_delete not in [i['teamid'] for i in data]

    def test_update_team(self):
        coach = baker.make("football.Coaches")  # Need a coach
        teams = baker.make("football.Teams", 10, coachid=coach)
        team: Teams = teams[2]

        r = self.client.get(f'/api/teams/{team.teamid}/')  # Use teamid
        data = r.json()
        assert data['name'] == team.name


        r = self.client.put(f'/api/teams/{team.teamid}/', {  # Use teamid
            "coachid": coach.coachid, # Important: Send the coachid
            "name": "Updated Team Name",
            "rating": 120,  # Example update
            "wins": 7,
            "losses": 1,
            "draws": 2, 
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/teams/{team.teamid}/')  # Use teamid
        data = r.json()
        assert data['name'] == "Updated Team Name"
        assert data['rating'] == 120  # Check updated rating

        team.refresh_from_db()
        assert data['name'] == team.name
        assert data['rating'] == team.rating # Check updated rating



class TournamentsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_tournaments(self):
        tournament = baker.make(
            "football.Tournaments",
            startdate=datetime(2024, 1, 1, tzinfo=timezone.utc),
            enddate=datetime(2024, 2, 1, tzinfo=timezone.utc)
        )

        r = self.client.get('/api/tournaments/')
        data = r.json()
        print(data)

        assert tournament.name == data[0]['name']
        assert tournament.tournamentid == data[0]['tournamentid']
        assert tournament.startdate.isoformat().replace('+00:00', 'Z') == data[0]['startdate']
        received_enddate = datetime.fromisoformat(data[0]['enddate'].replace('Z', '+00:00'))
        assert tournament.enddate == received_enddate

        assert tournament.rating == data[0]['rating']
        assert len(data) == 1

    def test_create_tournament(self):
        r = self.client.post("/api/tournaments/", {
            "name": "Test Tournament",
            "location": "Test Location",
            "startdate": "2024-01-01T00:00:00Z",
            "enddate": "2024-02-01T00:00:00Z",
            "rating": 100
        })
        data = r.json()
        new_tournament_id = r.json()['tournamentid']

        tournaments = Tournaments.objects.all()
        assert len(tournaments) == 1

        new_tournament = Tournaments.objects.filter(tournamentid=new_tournament_id).first()
        assert new_tournament.name == "Test Tournament"
        assert new_tournament.location == "Test Location"
        assert new_tournament.startdate == datetime(2024, 1, 1, tzinfo=timezone.utc)
        assert new_tournament.enddate == datetime(2024, 2, 1, tzinfo=timezone.utc)
        assert new_tournament.rating == 100



    def test_delete_tournament(self):
        tournaments = baker.make("football.Tournaments", 10, startdate=datetime(2024, 1, 1, tzinfo=timezone.utc), enddate=datetime(2024, 2, 1, tzinfo=timezone.utc))  # Create with dates
        r = self.client.get('/api/tournaments/')
        data = r.json()
        assert len(data) == 10

        tournament_id_to_delete = tournaments[3].tournamentid
        self.client.delete(f'/api/tournaments/{tournament_id_to_delete}/')

        r = self.client.get('/api/tournaments/')
        data = r.json()
        assert len(data) == 9

        assert tournament_id_to_delete not in [i['tournamentid'] for i in data]


    def test_update_tournament(self):
        tournaments = baker.make("football.Tournaments", 10, startdate=datetime(2024, 1, 1, tzinfo=timezone.utc), enddate=datetime(2024, 2, 1, tzinfo=timezone.utc))
        tournament: Tournaments = tournaments[2]

        r = self.client.get(f'/api/tournaments/{tournament.tournamentid}/')
        data = r.json()
        assert data['name'] == tournament.name

        r = self.client.put(f'/api/tournaments/{tournament.tournamentid}/', {
            "name": "Updated Tournament Name",
            "location": "Updated Location", # update location
            "startdate": "2025-03-05T10:00:00Z",  # Example update for startdate
            "enddate": "2025-04-10T12:30:00Z", # Example for enddate
            "rating": 150
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/tournaments/{tournament.tournamentid}/')
        data = r.json()
        assert data['name'] == "Updated Tournament Name"
        assert data["location"] == "Updated Location"
        assert data['startdate'] == "2025-03-05T10:00:00Z" # checking updated date
        assert data['enddate'] == "2025-04-10T12:30:00Z"
        assert data['rating'] == 150

        tournament.refresh_from_db()
        assert data['name'] == tournament.name
        assert data['location'] == tournament.location # checking updated location




class AthletesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_athletes(self):
        athlete = baker.make(
            "football.Athletes", 
            dateofbirth=datetime(2000, 1, 1, tzinfo=timezone.utc))
        r = self.client.get('/api/athletes/')
        data = r.json()
        print(data)

        assert athlete.fullname == data[0]['fullname']
        assert athlete.athleteid == data[0]['athleteid']
        assert athlete.dateofbirth.isoformat().replace('+00:00', 'Z') == data[0]['dateofbirth']
        assert athlete.weight == data[0]['weight']
        assert athlete.height == data[0]['height']
        assert athlete.gender == data[0]['gender']
        assert len(data) == 1



    def test_create_athlete(self):
        r = self.client.post("/api/athletes/", {
            "fullname": "Test Athlete",
            "dateofbirth": "1995-03-10T12:00:00Z",  # Example date
            "weight": 75.5,
            "height": 180,
            "gender": "Male"
        })
        data = r.json()
        new_athlete_id = data['athleteid']  # or 'id' if your serializer uses 'id'

        athletes = Athletes.objects.all()
        assert len(athletes) == 1

        new_athlete = Athletes.objects.get(athleteid=new_athlete_id)
        assert new_athlete.fullname == "Test Athlete"
        assert new_athlete.dateofbirth == datetime(1995, 3, 10, 12, 0, tzinfo=timezone.utc)
        assert new_athlete.weight == 75.5
        assert new_athlete.height == 180
        assert new_athlete.gender == "Male"


    def test_delete_athlete(self):
        athletes = baker.make("football.Athletes", 10, dateofbirth=datetime(2000, 1, 1, tzinfo=timezone.utc))
        r = self.client.get('/api/athletes/')
        data = r.json()
        assert len(data) == 10

        athlete_id_to_delete = athletes[3].athleteid
        self.client.delete(f'/api/athletes/{athlete_id_to_delete}/')

        r = self.client.get('/api/athletes/')
        data = r.json()
        assert len(data) == 9

        assert athlete_id_to_delete not in [i['athleteid'] for i in data] # or 'id'


    def test_update_athlete(self):
        athletes = baker.make("football.Athletes", 10, dateofbirth=datetime(2000, 1, 1, tzinfo=timezone.utc))
        athlete: Athletes = athletes[2]

        r = self.client.get(f'/api/athletes/{athlete.athleteid}/')
        data = r.json()
        assert data['fullname'] == athlete.fullname

        r = self.client.put(f'/api/athletes/{athlete.athleteid}/', {
            "fullname": "Updated Athlete Name",
            "dateofbirth": "1998-06-20T08:30:00Z",  # updated dateofbirth
            "weight": 80.2,  # update weight
            "height": 185,  # update height
            "gender": "Female"  # update gender
        })
        assert r.status_code == 200


        r = self.client.get(f'/api/athletes/{athlete.athleteid}/')
        data = r.json()
        assert data['fullname'] == "Updated Athlete Name"
        assert data['dateofbirth'] == "1998-06-20T08:30:00Z"  # Check the updated date
        assert data['weight'] == 80.2  # Check updated data
        assert data['height'] == 185
        assert data['gender'] == "Female"

        # Получаем обновлённый объект из базы данных
        updated_athlete = Athletes.objects.get(athleteid=athlete.athleteid)
        assert data['fullname'] == updated_athlete.fullname
        assert data['dateofbirth'] == updated_athlete.dateofbirth.isoformat().replace('+00:00', 'Z')


class ApplicationsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_applications(self):
        tournament = baker.make("football.Tournaments")
        application = baker.make("football.Applications", tournamentid=tournament)

        r = self.client.get('/api/applications/')
        data = r.json()
        print(data)

        assert application.status == data[0]['status']
        assert application.tournamentid.tournamentid == data[0]['tournamentid']  # Access through the relationship
        assert len(data) == 1

    def test_create_application(self):
        tournament = baker.make("football.Tournaments") # Create the related tournament first

        r = self.client.post("/api/applications/", {
            "tournamentid": tournament.tournamentid,  # Use tournamentid
            "status": "Submitted"
        })
        print(r.json())
        assert r.status_code == 201  # Check for successful creation

        data = r.json()
        new_application_id = data['applicationid'] # or 'id'

        applications = Applications.objects.all()
        assert len(applications) == 1

        new_application = Applications.objects.get(applicationid=new_application_id)  # Use applicationid
        assert new_application.status == "Submitted"
        assert new_application.tournamentid.tournamentid == tournament.tournamentid


    def test_delete_application(self):
        tournament = baker.make("football.Tournaments") # tournament needed for related field
        applications = baker.make("football.Applications", 10, tournamentid=tournament)  # Use tournamentid
        r = self.client.get('/api/applications/')
        data = r.json()
        assert len(data) == 10

        application_id_to_delete = applications[3].applicationid
        self.client.delete(f'/api/applications/{application_id_to_delete}/')

        r = self.client.get('/api/applications/')
        data = r.json()
        assert len(data) == 9

        assert application_id_to_delete not in [i['applicationid'] for i in data]  # or 'id'


    def test_update_application(self):
        tournament = baker.make("football.Tournaments") # tournament needed for related model
        applications = baker.make("football.Applications", 10, tournamentid=tournament)
        application: Applications = applications[2]

        r = self.client.get(f'/api/applications/{application.applicationid}/')  # Use applicationid
        data = r.json()
        assert data['status'] == application.status

        r = self.client.put(f'/api/applications/{application.applicationid}/', {  # Use applicationid
            "tournamentid": tournament.tournamentid, # Important: Send the correct tournamentid
            "status": "Approved"
        })
        assert r.status_code == 200


        r = self.client.get(f'/api/applications/{application.applicationid}/')
        data = r.json()
        assert data['status'] == "Approved"

        application.refresh_from_db()
        assert data['status'] == application.status  


class GamesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_games(self):
        tournament = baker.make("football.Tournaments")
        game = baker.make("football.Games", tournamentid=tournament, date=datetime(2024, 3, 15, 10, 30, tzinfo=timezone.utc))
        r = self.client.get('/api/games/')
        data = r.json()
        print(data)

        assert game.location == data[0]['location']
        assert game.gameid == data[0]['gameid']  # or 'id'
        assert game.tournamentid.tournamentid == data[0]['tournamentid']  # or 'id'
        assert game.date.isoformat().replace('+00:00', 'Z') == data[0]['date']
        assert game.score == data[0]['score']
        assert game.hierarchy == data[0]['hierarchy']
        assert len(data) == 1

    def test_create_game(self):
        tournament = baker.make("football.Tournaments")  # Create the related tournament
        r = self.client.post("/api/games/", {
            "tournamentid": tournament.tournamentid,  # Use tournamentid
            "date": "2024-03-15T10:30:00Z",
            "location": "Stadium A",
            "score": "2-1",
            "hierarchy": 1
        })
        print(r.json())  # для отладки
        assert r.status_code == 201

        data = r.json()
        new_game_id = data['gameid']  # or 'id'

        games = Games.objects.all()
        assert len(games) == 1

        new_game = Games.objects.get(gameid=new_game_id)
        assert new_game.tournamentid.tournamentid == tournament.tournamentid  # Access via relation
        assert new_game.date.isoformat().replace('+00:00', 'Z') == "2024-03-15T10:30:00Z"
        assert new_game.location == "Stadium A"
        assert new_game.score == "2-1"
        assert new_game.hierarchy == 1

    def test_delete_game(self):
        tournament = baker.make("football.Tournaments")
        games = baker.make("football.Games", 10, tournamentid=tournament, date=datetime(2024, 3, 15, 10, 30, tzinfo=timezone.utc))
        r = self.client.get('/api/games/')  # Check API endpoint
        data = r.json()
        assert len(data) == 10

        game_id_to_delete = games[3].gameid
        self.client.delete(f'/api/games/{game_id_to_delete}/')  # Check API endpoint

        r = self.client.get('/api/games/')  # Check API endpoint
        data = r.json()
        assert len(data) == 9

        assert game_id_to_delete not in [i['gameid'] for i in data]  # Or 'id'

    def test_update_game(self):
        tournament = baker.make("football.Tournaments")  # Tournament object for related field
        games = baker.make("football.Games", 10, tournamentid=tournament, date=datetime(2024, 3, 15, 10, 30, tzinfo=timezone.utc))
        game: Games = games[2]

        r = self.client.get(f'/api/games/{game.gameid}/')
        data = r.json()
        assert data['location'] == game.location

        r = self.client.put(f'/api/games/{game.gameid}/', {
            "tournamentid": tournament.tournamentid,  # Send the tournament ID
            "date": "2024-04-20T15:00:00Z",  # Updated date
            "location": "Stadium B",
            "score": "3-0",  # Updated score
            "hierarchy": 2  # Updated hierarchy
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/games/{game.gameid}/')
        data = r.json()
        assert data['date'] == "2024-04-20T15:00:00Z"  # Check the updated date string
        assert data['location'] == "Stadium B"  # Check other updated fields
        assert data['score'] == "3-0"
        assert data['hierarchy'] == 2

        # Получаем обновлённый объект из базы данных
        updated_game = Games.objects.get(gameid=game.gameid)
        assert updated_game.date.isoformat().replace('+00:00', 'Z') == "2024-04-20T15:00:00Z"
        assert updated_game.location == "Stadium B"
        assert updated_game.score == "3-0"
        assert updated_game.hierarchy == 2 


class TrainingsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_trainings(self):
        team = baker.make("football.Teams")
        training = baker.make("football.Trainings", teamid=team, date=datetime(2024, 4, 10, 9, 0, tzinfo=timezone.utc))
        r = self.client.get('/api/trainings/')
        data = r.json()
        print(data)

        assert training.name == data[0]['name']
        assert training.trainingid == data[0]['trainingid']  # Or 'id'
        assert training.teamid.teamid == data[0]['teamid']  # Or 'id'
        assert training.date.isoformat().replace('+00:00', 'Z') == data[0]['date']
        assert len(data) == 1

    def test_create_training(self):
        team = baker.make("football.Teams")
        r = self.client.post("/api/trainings/", {
            "teamid": team.teamid,  # Use teamid, or 'id' if your serializer uses that
            "name": "Test Training",
            "date": "2024-04-10T09:00:00Z"
        })
        data = r.json()
        assert r.status_code == 201

        new_training_id = data['trainingid']  # or 'id'

        trainings = Trainings.objects.all()
        assert len(trainings) == 1

        new_training = Trainings.objects.get(trainingid=new_training_id)
        assert new_training.name == "Test Training"
        assert new_training.teamid.teamid == team.teamid
        assert new_training.date.isoformat().replace('+00:00', 'Z') == "2024-04-10T09:00:00Z"

    def test_delete_training(self):
        team = baker.make("football.Teams")  # Team object for related field
        trainings = baker.make("football.Trainings", 10, teamid=team, date=datetime(2024, 4, 10, 9, 0, tzinfo=timezone.utc))
        r = self.client.get('/api/trainings/')  # Check the API endpoint
        data = r.json()
        assert len(data) == 10

        training_id_to_delete = trainings[3].trainingid
        self.client.delete(f'/api/trainings/{training_id_to_delete}/')

        r = self.client.get('/api/trainings/')  # Check the API endpoint
        data = r.json()
        assert len(data) == 9

        assert training_id_to_delete not in [i['trainingid'] for i in data]  # or 'id'

    def test_update_training(self):
        team = baker.make("football.Teams")  # Team needed for related field
        trainings = baker.make("football.Trainings", 10, teamid=team, date=datetime(2024, 4, 10, 9, 0, tzinfo=timezone.utc))
        training: Trainings = trainings[2]

        r = self.client.get(f'/api/trainings/{training.trainingid}/')  # Check API endpoint
        data = r.json()
        assert data['name'] == training.name

        r = self.client.put(f'/api/trainings/{training.trainingid}/', {
            "teamid": team.teamid,  # Correct teamid
            "name": "Updated Training",  # Updated name
            "date": "2024-04-15T11:30:00Z"  # Updated date and time string
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/trainings/{training.trainingid}/')
        data = r.json()
        assert data['name'] == "Updated Training"
        assert data['date'] == "2024-04-15T11:30:00Z"  # Check updated date string

        # Получаем обновлённый объект из базы данных
        updated_training = Trainings.objects.get(trainingid=training.trainingid)
        assert updated_training.name == "Updated Training"
        assert updated_training.date.isoformat().replace('+00:00', 'Z') == "2024-04-15T11:30:00Z"


class AttendanceViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_attendance(self):
        athlete = baker.make("football.Athletes")
        attendance = baker.make("football.Attendance", athleteid=athlete)
        r = self.client.get('/api/attendance/')
        data = r.json()
        print(data)

        assert attendance.attendanceid == data[0]['attendanceid']  # Or 'id'
        assert attendance.athleteid.athleteid == data[0]['athleteid']  # Or 'id'
        assert attendance.pressrating == data[0]['pressrating']
        assert attendance.captainrating == data[0]['captainrating']
        assert attendance.coachrating == data[0]['coachrating']
        assert len(data) == 1

    def test_create_attendance(self):
        athlete = baker.make("football.Athletes")
        r = self.client.post("/api/attendance/", {
            "athleteid": athlete.athleteid,  # Use athleteid, or 'id' if your serializer uses that
            "pressrating": 5,
            "captainrating": 4,
            "coachrating": 3
        })
        data = r.json()
        assert r.status_code == 201

        new_attendance_id = data['attendanceid']  # or 'id'

        attendances = Attendance.objects.all()
        assert len(attendances) == 1

        new_attendance = Attendance.objects.get(attendanceid=new_attendance_id)
        assert new_attendance.athleteid.athleteid == athlete.athleteid
        assert new_attendance.pressrating == 5
        assert new_attendance.captainrating == 4
        assert new_attendance.coachrating == 3

    def test_delete_attendance(self):
        athlete = baker.make("football.Athletes")  # Athlete object for related field
        attendances = baker.make("football.Attendance", 10, athleteid=athlete)
        r = self.client.get('/api/attendance/')  # Check the API endpoint
        data = r.json()
        assert len(data) == 10

        attendance_id_to_delete = attendances[3].attendanceid
        self.client.delete(f'/api/attendance/{attendance_id_to_delete}/')

        r = self.client.get('/api/attendance/')  # Check the API endpoint
        data = r.json()
        assert len(data) == 9

        assert attendance_id_to_delete not in [i['attendanceid'] for i in data]  # or 'id'

    def test_update_attendance(self):
        athlete = baker.make("football.Athletes")  # Athlete needed for related field
        attendances = baker.make("football.Attendance", 10, athleteid=athlete)
        attendance: Attendance = attendances[2]

        r = self.client.get(f'/api/attendance/{attendance.attendanceid}/')  # Check API endpoint
        data = r.json()
        assert data['pressrating'] == attendance.pressrating

        r = self.client.put(f'/api/attendance/{attendance.attendanceid}/', {
            "athleteid": athlete.athleteid,  # Correct athleteid
            "pressrating": 8,  # Updated pressrating
            "captainrating": 7,  # Updated captainrating
            "coachrating": 6  # Updated coachrating
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/attendance/{attendance.attendanceid}/')
        data = r.json()
        assert data['pressrating'] == 8
        assert data['captainrating'] == 7
        assert data['coachrating'] == 6

        # Получаем обновлённый объект из базы данных
        updated_attendance = Attendance.objects.get(attendanceid=attendance.attendanceid)
        assert updated_attendance.pressrating == 8
        assert updated_attendance.captainrating == 7
        assert updated_attendance.coachrating == 6


class ResultsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_results(self):
        athlete = baker.make("football.Athletes")
        result = baker.make("football.Results", athleteid=athlete)
        r = self.client.get('/api/results/')
        data = r.json()
        print(data)

        assert result.resultid == data[0]['resultid']  # Or 'id'
        assert result.athleteid.athleteid == data[0]['athleteid']  # Or 'id'
        assert result.athleteplace == data[0]['athleteplace']
        assert result.goalsscored == data[0]['goalsscored']
        assert len(data) == 1

    def test_create_result(self):
        athlete = baker.make("football.Athletes")
        r = self.client.post("/api/results/", {
            "athleteid": athlete.athleteid,  # Use athleteid, or 'id' if your serializer uses that
            "athleteplace": 1,
            "goalsscored": 3
        })
        data = r.json()
        assert r.status_code == 201

        new_result_id = data['resultid']  # or 'id'

        results = Results.objects.all()
        assert len(results) == 1

        new_result = Results.objects.get(resultid=new_result_id)
        assert new_result.athleteid.athleteid == athlete.athleteid
        assert new_result.athleteplace == 1
        assert new_result.goalsscored == 3

    def test_delete_result(self):
        athlete = baker.make("football.Athletes")  # Athlete object for related field
        results = baker.make("football.Results", 10, athleteid=athlete)
        r = self.client.get('/api/results/')  # Check the API endpoint
        data = r.json()
        assert len(data) == 10

        result_id_to_delete = results[3].resultid
        self.client.delete(f'/api/results/{result_id_to_delete}/')

        r = self.client.get('/api/results/')  # Check the API endpoint
        data = r.json()
        assert len(data) == 9

        assert result_id_to_delete not in [i['resultid'] for i in data]  # or 'id'

    def test_update_result(self):
        athlete = baker.make("football.Athletes")  # Athlete needed for related field
        results = baker.make("football.Results", 10, athleteid=athlete)
        result: Results = results[2]

        r = self.client.get(f'/api/results/{result.resultid}/')  # Check API endpoint
        data = r.json()
        assert data['athleteplace'] == result.athleteplace

        r = self.client.put(f'/api/results/{result.resultid}/', {
            "athleteid": athlete.athleteid,  # Correct athleteid
            "athleteplace": 2,  # Updated athleteplace
            "goalsscored": 5  # Updated goalsscored
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/results/{result.resultid}/')
        data = r.json()
        assert data['athleteplace'] == 2
        assert data['goalsscored'] == 5

        # Получаем обновлённый объект из базы данных
        updated_result = Results.objects.get(resultid=result.resultid)
        assert updated_result.athleteplace == 2
        assert updated_result.goalsscored == 5


class TeamsingamesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list_teamsingames(self):
        team = baker.make("football.Teams")
        game = baker.make("football.Games")
        teamsingame = baker.make("football.Teamsingames", teamid=team, gameid=game)
        r = self.client.get('/api/teamsingames/')
        data = r.json()
        print(data)

        assert teamsingame.teamid.teamid == data[0]['teamid']  # Or 'id'
        assert teamsingame.gameid.gameid == data[0]['gameid']  # Or 'id'
        assert len(data) == 1

    def test_create_teamsingame(self):
        team = baker.make("football.Teams")
        game = baker.make("football.Games")
        r = self.client.post("/api/teamsingames/", {
            "teamid": team.teamid,  # Use teamid, or 'id' if your serializer uses that
            "gameid": game.gameid  # Use gameid, or 'id' if your serializer uses that
        })
        data = r.json()
        assert r.status_code == 201

        new_teamsingame_teamid = data['teamid']  # or 'id'
        new_teamsingame_gameid = data['gameid']  # or 'id'

        teamsingames = Teamsingames.objects.all()
        assert len(teamsingames) == 1

        new_teamsingame = Teamsingames.objects.get(teamid=new_teamsingame_teamid, gameid=new_teamsingame_gameid)
        assert new_teamsingame.teamid.teamid == team.teamid
        assert new_teamsingame.gameid.gameid == game.gameid


    def test_delete_teamsingame(self):
        teamsingame = baker.make("football.Teamsingames", 10)
        r = self.client.get("/api/teamsingames/")
        data = r.json()
        assert len(data) == 10

        # Удаляем запись через API
        teamsingame_id_to_delete = teamsingame[3].teamsingameid
        self.client.delete(f'/api/teamsingames/{teamsingame_id_to_delete}/')
        
        r = self.client.get("/api/teamsingames/")
        data = r.json()
        assert len(data) == 9

        assert teamsingame_id_to_delete not in [i['teamsingameid'] for i in data] 


    def test_update_teamsingame(self):
        team = baker.make("football.Teams")
        game = baker.make("football.Games")
        teamsingames_list = baker.make("football.Teamsingames", 10, teamid=team, gameid=game)
        teamsingames: Teamsingames = teamsingames_list[2]


        r = self.client.get(f'/api/teamsingames/{teamsingames.teamsingameid}/')  
        data = r.json()
        assert data['teamid'] == teamsingames.teamid.teamid  
        assert data['gameid'] == teamsingames.gameid.gameid 

        new_team = baker.make("football.Teams")
        new_game = baker.make("football.Games")

        # Обновляем данные через API
        r = self.client.put(f'/api/teamsingames/{teamsingames.teamsingameid}/', {
            "teamid": new_team.teamid, 
            "gameid": new_game.gameid 
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/teamsingames/{teamsingames.teamsingameid}/')
        data = r.json()
        assert data['teamid'] == new_team.teamid
        assert data['gameid'] == new_game.gameid

        # Проверяем, что данные обновились в базе данных
        updated_teamsingames = Teamsingames.objects.get(teamsingameid=teamsingames.teamsingameid)
        assert updated_teamsingames.teamid.teamid == new_team.teamid
        assert updated_teamsingames.gameid.gameid == new_game.gameid
       