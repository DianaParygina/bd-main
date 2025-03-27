from django.db import models


class Applications(models.Model):
    applicationid = models.AutoField(db_column='ApplicationID', primary_key=True)  # Field name made lowercase.
    tournamentid = models.ForeignKey('Tournaments', models.DO_NOTHING, db_column='TournamentID', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Applications'


class Athletes(models.Model):
    athleteid = models.AutoField(db_column='AthleteID', primary_key=True)
    fullname = models.CharField(db_column='FullName', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)
    weight = models.IntegerField(db_column='Weight', blank=True, null=True) 
    height = models.IntegerField(db_column='Height', blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=10, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Athletes'


class Attendance(models.Model):
    attendanceid = models.AutoField(db_column='AttendanceID', primary_key=True)  # Field name made lowercase.
    athleteid = models.ForeignKey(Athletes, models.DO_NOTHING, db_column='AthleteID', blank=True, null=True)  # Field name made lowercase.
    pressrating = models.IntegerField(db_column='PressRating', blank=True, null=True)  # Field name made lowercase.
    captainrating = models.IntegerField(db_column='CaptainRating', blank=True, null=True)  # Field name made lowercase.
    coachrating = models.IntegerField(db_column='CoachRating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Attendance'


class Coaches(models.Model):
    coachid = models.AutoField(db_column='CoachID', primary_key=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Coaches'


class Games(models.Model):
    gameid = models.AutoField(db_column='GameID', primary_key=True)  # Field name made lowercase.
    tournamentid = models.ForeignKey('Tournaments', models.DO_NOTHING, db_column='TournamentID', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    score = models.CharField(db_column='Score', max_length=50, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    hierarchy = models.IntegerField(db_column='Hierarchy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Games'


class Results(models.Model):
    resultid = models.AutoField(db_column='ResultID', primary_key=True)  # Field name made lowercase.
    athleteid = models.ForeignKey(Athletes, models.DO_NOTHING, db_column='AthleteID', blank=True, null=True)  # Field name made lowercase.
    athleteplace = models.IntegerField(db_column='AthletePlace', blank=True, null=True)  # Field name made lowercase.
    goalsscored = models.IntegerField(db_column='GoalsScored', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Results'


class Teams(models.Model):
    teamid = models.AutoField(db_column='TeamID', primary_key=True)  # Field name made lowercase.
    coachid = models.ForeignKey(Coaches, models.DO_NOTHING, db_column='CoachID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    wins = models.IntegerField(db_column='Wins', blank=True, null=True)  # Field name made lowercase.
    losses = models.IntegerField(db_column='Losses', blank=True, null=True)  # Field name made lowercase.
    draws = models.IntegerField(db_column='Draws', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Teams'


class Teamsingames(models.Model):
    teamsingameid = models.AutoField(db_column='TeamsingameID', primary_key=True) 
    teamid = models.ForeignKey(Teams, models.DO_NOTHING, db_column='TeamID')  
    gameid = models.ForeignKey(Games, models.DO_NOTHING, db_column='GameID')

    class Meta:
        managed = True
        db_table = 'TeamsInGames'


class Tournaments(models.Model):
    tournamentid = models.AutoField(db_column='TournamentID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Tournaments'


class Trainings(models.Model):
    trainingid = models.AutoField(db_column='TrainingID', primary_key=True)  # Field name made lowercase.
    teamid = models.ForeignKey(Teams, models.DO_NOTHING, db_column='TeamID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255, db_collation='Cyrillic_General_CI_AS', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Trainings'


















# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150, db_collation='Cyrillic_General_CI_AS')

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100, db_collation='Cyrillic_General_CI_AS')

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128, db_collation='Cyrillic_General_CI_AS')
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField()
#     username = models.CharField(unique=True, max_length=150, db_collation='Cyrillic_General_CI_AS')
#     first_name = models.CharField(max_length=150, db_collation='Cyrillic_General_CI_AS')
#     last_name = models.CharField(max_length=150, db_collation='Cyrillic_General_CI_AS')
#     email = models.CharField(max_length=254, db_collation='Cyrillic_General_CI_AS')
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(db_collation='Cyrillic_General_CI_AS', blank=True, null=True)
#     object_repr = models.CharField(max_length=200, db_collation='Cyrillic_General_CI_AS')
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField(db_collation='Cyrillic_General_CI_AS')
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100, db_collation='Cyrillic_General_CI_AS')
#     model = models.CharField(max_length=100, db_collation='Cyrillic_General_CI_AS')

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
#     name = models.CharField(max_length=255, db_collation='Cyrillic_General_CI_AS')
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40, db_collation='Cyrillic_General_CI_AS')
#     session_data = models.TextField(db_collation='Cyrillic_General_CI_AS')
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'
