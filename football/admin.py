from django.contrib import admin
from .models import Tournaments, Applications, Coaches, Teams, Games, Teamsingames, Athletes, Results, Trainings, Attendance

# Регистрация моделей
admin.site.register(Tournaments)
admin.site.register(Applications)
admin.site.register(Coaches)
admin.site.register(Teams)
admin.site.register(Games)
admin.site.register(Teamsingames)
admin.site.register(Athletes)
admin.site.register(Results)
admin.site.register(Trainings)
admin.site.register(Attendance)