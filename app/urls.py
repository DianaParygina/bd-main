"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, AthleteList, AthleteDetail
from .views import (
    ApplicationsViewSet, AthletesViewSet, AttendanceViewSet,
    CoachesViewSet, GamesViewSet, ResultsViewSet, TeamsViewSet,
    TeamsInGamesViewSet, TournamentsViewSet, TrainingsViewSet
)

router = DefaultRouter()
router.register(r'applications', ApplicationsViewSet)
router.register(r'athletes', AthletesViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'coaches', CoachesViewSet)
router.register(r'games', GamesViewSet)
router.register(r'results', ResultsViewSet)
router.register(r'teams', TeamsViewSet)
router.register(r'teamsingames', TeamsInGamesViewSet)
router.register(r'tournaments', TournamentsViewSet)
router.register(r'trainings', TrainingsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Подключение административной панели
    path('athletes/', AthleteList.as_view(), name='athlete-list'),
    path('athletes/<int:pk>/', AthleteDetail.as_view(), name='athlete-detail'),
    path('home/', home, name='home'),
    path('api/', include(router.urls)),
]