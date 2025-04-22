from rest_framework import viewsets, filters, generics, status
from django.http import HttpResponse
from django.db.models import Q, F, Count
from django.db import connection
from rest_framework.response import Response
from django.db.models import Count
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
    queryset = Athletes.objects.all()
    filterset_fields = ['dateofbirth', 'weight', 'height']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()) # Используйте filter_queryset для корректной работы с пагинацией и фильтрацией

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset) #  Важно для сохранения стандартной функциональности filter_queryset
        year_gt = self.request.query_params.get('dateofbirth__year__gt')
        weight = self.request.query_params.get('weight')
        height = self.request.query_params.get('height')


        if year_gt:
            try:
                year_gt = int(year_gt)
                queryset = queryset.filter(dateofbirth__year__gt=year_gt)
            except (ValueError, TypeError):
                return queryset.none() # Лучше вернуть пустой QuerySet, чтобы не сломать фильтрацию.

        if weight:
             try:
                 weight = int(weight)
                 queryset = queryset.filter(weight=weight)
             except (ValueError, TypeError):
                 return queryset.none() 
             
        if height:
             try:
                 height = int(height)
                 queryset = queryset.filter(height=height)
             except (ValueError, TypeError):
                 return queryset.none()      

        return queryset


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()
    filterset_fields = ['pressrating', 'captainrating', 'coachrating']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        pressrating = self.request.query_params.get('pressrating')
        captainrating = self.request.query_params.get('captainrating')
        coachrating = self.request.query_params.get('coachrating')


        if pressrating:
            try:
                pressrating = int(pressrating)  # или float, в зависимости от типа поля
                queryset = queryset.filter(pressrating=pressrating)
            except (ValueError, TypeError):
                return queryset.none()

        if captainrating:
            try:
                captainrating = int(captainrating)  # или float
                queryset = queryset.filter(captainrating=captainrating)
            except (ValueError, TypeError):
                return queryset.none()

        if coachrating:
            try:
                coachrating = int(coachrating)  # или float
                queryset = queryset.filter(coachrating=coachrating)
            except (ValueError, TypeError):
                return queryset.none()

        return queryset


class CoachesViewSet(viewsets.ModelViewSet):
    serializer_class = CoachesSerializer
    queryset = Coaches.objects.all()
    filterset_fields = ['fullname', 'dateofbirth']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        fullname_contains = self.request.query_params.get('fullname__contains')
        dateofbirth_year_lt = self.request.query_params.get('dateofbirth__year__lt')
        # Другие параметры фильтрации, если нужны

        if fullname_contains:
            queryset = queryset.filter(fullname__icontains=fullname_contains)

        if dateofbirth_year_lt:
            try:
                dateofbirth_year_lt = int(dateofbirth_year_lt)
                queryset = queryset.filter(dateofbirth__year__lt=dateofbirth_year_lt)
            except (ValueError, TypeError):
                return queryset.none()

        return queryset
    

class GamesViewSet(viewsets.ModelViewSet):
    serializer_class = GamesSerializer
    queryset = Games.objects.all()
    filterset_fields = ['date', 'score', 'hierarchy']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        date_year_gt = self.request.query_params.get('date__year__gt')
        date_year_lt = self.request.query_params.get('date__year__lt')
        date = self.request.query_params.get('date')  # Точное совпадение по дате
        score = self.request.query_params.get('score')       # Точное совпадение по счету
        score_contains = self.request.query_params.get('score__contains') #  Поиск подстроки в счете
        hierarchy = self.request.query_params.get('hierarchy') #  Точное совпадение по hierarchy


        if date_year_gt:
            try:
                date_year_gt = int(date_year_gt)
                queryset = queryset.filter(date__year__gt=date_year_gt)
            except (ValueError, TypeError):
                return queryset.none()

        if date_year_lt:
            try:
                date_year_lt = int(date_year_lt)
                queryset = queryset.filter(date__year__lt=date_year_lt)
            except (ValueError, TypeError):
                return queryset.none()


        if date:
            try:
                # date = date.strptime(date, '%Y-%m-%d').date() #  Укажите формат даты, соответствующий вашим данным!
                queryset = queryset.filter(date=date)
            except (ValueError, TypeError):
                return queryset.none()
        
        if score:
             queryset = queryset.filter(score=score) # Предполагается, что score - строка

        if score_contains:
            queryset = queryset.filter(score__icontains=score_contains)

        if hierarchy:
            queryset = queryset.filter(hierarchy=hierarchy)


        return queryset
    

class ResultsViewSet(viewsets.ModelViewSet):
    serializer_class = ResultsSerializer
    queryset = Results.objects.all()
    filterset_fields = ['athleteplace', 'goalsscored']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        athleteplace = self.request.query_params.get('athleteplace')
        goalsscored = self.request.query_params.get('goalsscored')
        # athleteid = self.request.query_params.get('athleteid')

        if athleteplace:
            try:
                athleteplace = int(athleteplace)
                queryset = queryset.filter(athleteplace=athleteplace)
            except (ValueError, TypeError):
                return queryset.none()

        if goalsscored:
            try:
                goalsscored = int(goalsscored)
                queryset = queryset.filter(goalsscored=goalsscored)
            except (ValueError, TypeError):
                return queryset.none()

        return queryset
    

class TeamsViewSet(viewsets.ModelViewSet):
    serializer_class = TeamsSerializer
    queryset = Teams.objects.all()
    filterset_fields = ['wins', 'losses']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        wins = self.request.query_params.get('wins')
        losses = self.request.query_params.get('losses')
        wins_gt = self.request.query_params.get('wins__gt')
        losses_lt = self.request.query_params.get('losses__lt')

        if wins:
            try:
                wins = int(wins)
                queryset = queryset.filter(wins=wins)
            except (ValueError, TypeError):
                return queryset.none()

        if losses:
            try:
                losses = int(losses)
                queryset = queryset.filter(losses=losses)
            except (ValueError, TypeError):
                return queryset.none()

        if wins_gt:
            try:
                wins_gt = int(wins_gt)
                queryset = queryset.filter(wins__gt=wins_gt)
            except (ValueError, TypeError):
                return queryset.none()

        if losses_lt:
            try:
                losses_lt = int(losses_lt)
                queryset = queryset.filter(losses__lt=losses_lt)
            except (ValueError, TypeError):
                return queryset.none()

        return queryset



class TeamsInGamesViewSet(viewsets.ModelViewSet):
    serializer_class = TeamsInGamesSerializer
    queryset = Teamsingames.objects.all()

    def list(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 100))
        try:
            queryset = self.filter_queryset(self.get_queryset())[:limit] #  ограничиваем количество результатов
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except (ValueError, TypeError) as e: #  обрабатываем ошибки, если limit не число
            return Response({"error": "Invalid limit parameter"}, status=status.HTTP_400_BAD_REQUEST)
        

class TournamentsViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentsSerializer
    queryset = Tournaments.objects.all()
    filterset_fields = ['startdate', 'rating']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        startdate_year_gt = self.request.query_params.get('startdate__year__gt')
        rating = self.request.query_params.get('rating')
        rating_gt = self.request.query_params.get('rating__gt')
        rating_lt = self.request.query_params.get('rating__lt')

        if startdate_year_gt:
            try:
                startdate_year_gt = int(startdate_year_gt)
                queryset = queryset.filter(startdate__year__gt=startdate_year_gt)
            except (ValueError, TypeError):
                return queryset.none()

        if rating:
            try:
                rating = int(rating)  # Или float, если rating - не целое число
                queryset = queryset.filter(rating=rating)
            except (ValueError, TypeError):
                return queryset.none()

        if rating_gt:
            try:
                rating_gt = int(rating_gt)  # Или float
                queryset = queryset.filter(rating__gt=rating_gt)
            except (ValueError, TypeError):
                return queryset.none()

        if rating_lt:
            try:
                rating_lt = int(rating_lt)  # Или float
                queryset = queryset.filter(rating__lt=rating_lt)
            except (ValueError, TypeError):
                return queryset.none()

        return queryset


class TrainingsViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingsSerializer
    queryset = Trainings.objects.all()
    filterset_fields = ['date']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        date_year_gt = self.request.query_params.get('date__year__gt')
        teamid = self.request.query_params.get('teamid')
        trainingid = self.request.query_params.get('trainingid')

        if date_year_gt:
            try:
                date_year_gt = int(date_year_gt)
                queryset = queryset.filter(date__year__gt=date_year_gt)
            except (ValueError, TypeError):
                return queryset.none()

        if teamid:
            try:
                teamid = int(teamid)
                queryset = queryset.filter(teamid=teamid)
            except (ValueError, TypeError):
                return queryset.none()

        if trainingid:
            try:
                trainingid = int(trainingid)
                queryset = queryset.filter(trainingid=trainingid)
            except (ValueError, TypeError):
                return queryset.none()

        return queryset



class AthleteList(generics.ListCreateAPIView):
    queryset = Athletes.objects.all()
    serializer_class = AthletesSerializer


class AthleteDetail(generics.RetrieveAPIView):
    queryset = Athletes.objects.all()
    serializer_class = AthletesSerializer


class AthletesInGamesViewSet(viewsets.ViewSet): # ViewSet для произвольных запросов
    def list(self, request):
        game_id = request.query_params.get('gameid')

        # Джоин Athletes, Results, TeamsInGames и Games
        queryset = Athletes.objects.filter(
            resultid__gameid=game_id  # Связь через промежуточную таблицу Results
        ).values(
            'athleteid', 'fullname', 'resultid__goalsscored', 'resultid__athleteplace', 'resultid__gameid__date', 'resultid__gameid__location'
        )

        serializer = AthletesSerializer(queryset, many=True, context={'request': request}) # Используем AthletesSerializer
        return Response(serializer.data)



class TrainingsByTeamViewSet(viewsets.ViewSet):
    def list(self, request):
        team_id = request.query_params.get('teamid')

        # Джоин Trainings и Teams, а также подсчет количества тренировок
        queryset = Teams.objects.filter(
            teamid=team_id
        ).annotate(
            trainings_count=Count('trainings')
        ).values(
            'teamid', 'name', 'trainings_count'
        )


        serializer = TeamsSerializer(queryset, many=True, context={'request': request}) # Используем TeamsSerializer
        return Response(serializer.data)



def home(request):
    return HttpResponse("Добро пожаловать на главную страницу!")


class AthletesTrainingsViewSet(viewsets.ViewSet):
    def list(self, request):
        # Получаем параметры фильтрации из запроса
        birth_year = request.query_params.get('birth_year', 1990)
        training_year = request.query_params.get('training_year', 2023)
        
        # Основной запрос с фильтрацией
        queryset = Athletes.objects.filter(
            gender='Male',
            dateofbirth__year=birth_year,
            attendance__isnull=False,  # Проверка наличия записи в Attendance
            teamid__trainings__date__year=training_year
        ).annotate(
            TeamName=F('teamid__name'),
            TrainingName=F('teamid__trainings__name'),
            TrainingDate=F('teamid__trainings__date')
        ).values(
            'athleteid',
            'fullname',
            'dateofbirth',
            'TeamName',
            'TrainingName',
            'TrainingDate'
        ).order_by('fullname', 'TrainingDate')

        # Форматируем результаты в плоскую структуру как в SQL
        results = [{
            'AthleteName': item['fullname'],
            'DateOfBirth': item['dateofbirth'],
            'TrainingName': item['TrainingName'],
            'TrainingDate': item['TrainingDate'],
            'TeamName': item['TeamName']
        } for item in queryset]

        return Response({
            'results': results,
            'filters': {
                'birth_year': birth_year,
                'training_year': training_year
            }
        })


class CoachesTournamentsViewSet(viewsets.ViewSet):
    def list(self, request):
        # Получаем параметры фильтрации из запроса
        coach_birth_year = request.query_params.get('coach_birth_year', 1970)
        tournament_year = request.query_params.get('tournament_year', 2023)
        
        # Основной запрос с фильтрацией
        queryset = Coaches.objects.filter(
            dateofbirth__year=coach_birth_year,
            teams__teamsingames__gameid__tournamentid__startdate__year=tournament_year
        ).annotate(
            TeamName=F('teams__name'),
            GameLocation=F('teams__teamsingames__gameid__location'),
            TournamentName=F('teams__teamsingames__gameid__tournamentid__name'),
            TournamentStart=F('teams__teamsingames__gameid__tournamentid__startdate')
        ).values(
            'fullname',
            'dateofbirth',
            'TeamName',
            'GameLocation',
            'TournamentName',
            'TournamentStart'
        ).order_by('fullname', 'TournamentStart')

        # Форматируем результаты в плоскую структуру как в SQL
        results = [{
            'CoachName': item['fullname'],
            'DateOfBirth': item['dateofbirth'],
            'TeamName': item['TeamName'],
            'GameLocation': item['GameLocation'],
            'TournamentName': item['TournamentName'],
            'TournamentStart': item['TournamentStart']
        } for item in queryset]

        return Response({
            'results': results,
            'filters': {
                'coach_birth_year': coach_birth_year,
                'tournament_year': tournament_year
            }
        })