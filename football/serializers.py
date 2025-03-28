from rest_framework import serializers
from .models import (
    Applications, Athletes, Attendance, Coaches, Games, Results,
    Teams, Teamsingames, Tournaments, Trainings
)

class ApplicationsSerializer(serializers.ModelSerializer):
    dateofbirth = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = Applications
        fields = ('applicationid', 'tournamentid', 'status') 

class AthletesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athletes
        fields = ('athleteid', 'fullname', 'dateofbirth', 'weight', 'height')

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('attendanceid', 'athleteid', 'pressrating', 'captainrating', 'coachrating')

class CoachesSerializer(serializers.ModelSerializer):
    dateofbirth = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Coaches
        fields = ('coachid', 'fullname', 'dateofbirth')

class GamesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Games
        fields = ('gameid', 'tournamentid', 'date', 'location', 'score', 'hierarchy')

class ResultsSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='athleteid.fullname', read_only=True)
                                     
    class Meta:
        model = Results
        fields = ('resultid', 'athleteid', 'athleteplace', 'goalsscored', 'fullname')

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ('teamid', 'coachid', 'name', 'rating', 'wins', 'losses', 'draws')

class TeamsInGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teamsingames
        fields = '__all__'

class TournamentsSerializer(serializers.ModelSerializer):
    startdate = serializers.DateField(format="%Y-%m-%d")
    enddate = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Tournaments
        fields = ('tournamentid', 'name', 'location', 'startdate', 'enddate', 'rating')

class TrainingsSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")
    
    class Meta:
        model = Trainings
        fields = ('trainingid', 'teamid', 'name', 'date')



# class AthletesWithTournamentsSerializer(serializers.Serializer):  # Используйте Serializer, а не ModelSerializer
    # athleteid = serializers.IntegerField()
    # fullname = serializers.CharField()
    # tournament_name = serializers.CharField(source='results_set__gameid__tournamentid__name')
    # tournament_location = serializers.CharField(source='results_set__gameid__tournamentid__location')
    # tournament_startdate = serializers.DateField(source='results_set__gameid__tournamentid__startdate')
    # tournament_enddate = serializers.DateField(source='results_set__gameid__tournamentid__enddate')