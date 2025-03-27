from rest_framework import viewsets, filters, generics
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from football.models import (
    Applications, Athletes, Attendance, Coaches, Games, Results,
    Teams, Teamsingames, Tournaments, Trainings
)
from football.serializers import (
    ApplicationsSerializer, AthletesSerializer, AttendanceSerializer,
    CoachesSerializer, GamesSerializer, ResultsSerializer, TeamsSerializer,
    TeamsInGamesSerializer, TournamentsSerializer, TrainingsSerializer
)



class ApplicationsViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournamentid', 'status']
    queryset = Applications.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        tournamentid = self.request.query_params.get('tournamentid__gt', None)
        status = self.request.query_params.get('status', None)

        if tournamentid:
            queryset = queryset.filter(tournamentid__gt=tournamentid)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class AthletesViewSet(viewsets.ModelViewSet):
    serializer_class = AthletesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['athleteid', 'dateofbirth', 'weight', 'height']
    queryset = Athletes.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        year = self.request.query_params.get('dateofbirth__year__gt', None)
        weight = self.request.query_params.get('weight', None)
        height = self.request.query_params.get('height', None)
        athleteid = self.request.query_params.get('athleteid__gt', None)

        if year:
            queryset = queryset.filter(dateofbirth__year__gt=year)
        if weight:
            queryset = queryset.filter(weight=weight)
        if height:
            queryset = queryset.filter(height=height)
        if athleteid:
            queryset = queryset.filter(athleteid__gt=athleteid)    

        return queryset


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pressrating', 'captainrating', 'coachrating', 'athleteid']
    queryset = Attendance.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        pressrating = self.request.query_params.get('pressrating', None)
        captainrating = self.request.query_params.get('captainrating', None)
        coachrating = self.request.query_params.get('coachrating', None)
        athleteid = self.request.query_params.get('athleteid__gt', None)

        if pressrating:
            queryset = queryset.filter(pressrating=pressrating)
        if captainrating:
            queryset = queryset.filter(captainrating=captainrating)
        if coachrating:
            queryset = queryset.filter(coachrating=coachrating)
        if athleteid:
            queryset = queryset.filter(athleteid__gt=athleteid)    

        return queryset


class CoachesViewSet(viewsets.ModelViewSet):
    serializer_class = CoachesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fullname', 'dateofbirth']
    queryset = Coaches.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        fullname = self.request.query_params.get('fullname__contains', None)
        year = self.request.query_params.get('dateofbirth__year__lt', None)

        if fullname:
            queryset = queryset.filter(fullname__contains=fullname)
        if year:
            queryset = queryset.filter(dateofbirth__year__lt=year)  

        return queryset


class GamesViewSet(viewsets.ModelViewSet):
    serializer_class = GamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tournamentid', 'date', 'score', 'hierarchy']
    queryset = Games.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        date = self.request.query_params.get('date__year__gt', None)
        score = self.request.query_params.get('score', None)
        hierarchy = self.request.query_params.get('hierarchy', None)
        tournamentid = self.request.query_params.get('tournamentid__gt', None)

        if date:
            queryset = queryset.filter(date__year__gt=date)
        if score:
            queryset = queryset.filter(score=score)
        if hierarchy:
            queryset = queryset.filter(hierarchy=hierarchy)
        if tournamentid:
            queryset = queryset.filter(tournamentid__gt=tournamentid)    

        return queryset
    

class ResultsViewSet(viewsets.ModelViewSet):
    serializer_class = ResultsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['athleteplace', 'goalsscored', 'athleteid']
    queryset = Results.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        athleteplace = self.request.query_params.get('athleteplace', None)
        goalsscored = self.request.query_params.get('goalsscored', None)
        athleteid = self.request.query_params.get('athleteid__lt', None)

        if athleteplace:
            queryset = queryset.filter(athleteplace=athleteplace)
        if goalsscored:
            queryset = queryset.filter(goalsscored=goalsscored)
        if athleteid:
            queryset = queryset.filter(athleteid__lt=athleteid)

        return queryset


class TeamsViewSet(viewsets.ModelViewSet):
    serializer_class = TeamsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wins', 'losses']
    queryset = Teams.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        wins = self.request.query_params.get('wins', None)
        losses = self.request.query_params.get('losses', None)

        if wins:
            queryset = queryset.filter(wins=wins)
        if losses:
            queryset = queryset.filter(losses=losses)

        return queryset


class TeamsInGamesViewSet(viewsets.ModelViewSet):
    serializer_class = TeamsInGamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['teamid', 'gameid']
    queryset = Teamsingames.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        teamid = self.request.query_params.get('teamid', None)
        gameid = self.request.query_params.get('gameid', None)

        if teamid:
            queryset = queryset.filter(teamid=teamid)
        if gameid:
            queryset = queryset.filter(gameid=gameid)

        return queryset


class TournamentsViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['startdate', 'rating']
    queryset = Tournaments.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        startdate = self.request.query_params.get('startdate__year__gt', None)
        rating = self.request.query_params.get('rating', None)

        if startdate:
            queryset = queryset.filter(startdate__year__gt=startdate)
        if rating:
            queryset = queryset.filter(rating=rating)

        return queryset


class TrainingsViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
    queryset = Trainings.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        # tournamentid = self.request.query_params.get('tournamentid__gt', None)
        date = self.request.query_params.get('date__year__gt', None)

        # if tournamentid:
        #     queryset = queryset.filter(tournamentid__gt=tournamentid)
        if date:
            queryset = queryset.filter(date__year__gt=date)

        return queryset


class AthleteList(generics.ListCreateAPIView):
    queryset = Athletes.objects.all()
    serializer_class = AthletesSerializer


class AthleteDetail(generics.RetrieveAPIView):
    queryset = Athletes.objects.all()
    serializer_class = AthletesSerializer


def home(request):
    return HttpResponse("Добро пожаловать на главную страницу!")