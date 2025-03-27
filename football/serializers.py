from rest_framework import serializers
from .models import (
    Applications, Athletes, Attendance, Coaches, Games, Results,
    Teams, Teamsingames, Tournaments, Trainings
)

class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = '__all__'

class AthletesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athletes
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class CoachesSerializer(serializers.ModelSerializer):
    dateofbirth = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Coaches
        fields = '__all__'

class GamesSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Games
        fields = '__all__'

class ResultsSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='athleteid.fullname', read_only=True)
                                     
    class Meta:
        model = Results
        fields = '__all__'

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = '__all__'

class TeamsInGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teamsingames
        fields = '__all__'

class TournamentsSerializer(serializers.ModelSerializer):
    startdate = serializers.DateField(format="%Y-%m-%d")
    enddate = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Tournaments
        fields = '__all__'

class TrainingsSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d")
    
    class Meta:
        model = Trainings
        fields = '__all__'