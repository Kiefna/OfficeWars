from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from tinymce.models import HTMLField


# Create your models here.
class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):  # Python 3.3 is __str__
        return self.email


class War(models.Model):
    TOURNAMENT = 'TM'
    LEADERBOARD = 'LB'
    PUZZLE = 'PZ'

    WAR_CHOICES = (
        (TOURNAMENT, "Tournament"),
        (LEADERBOARD, "Leaderboard"),
        (PUZZLE, "Puzzle"),
    )

    war_name = models.CharField("War Name", max_length=100)
    war_type = models.CharField("Type of War", max_length=2, choices=WAR_CHOICES, default=TOURNAMENT)
    # status = models.BooleanField("Starts Immediately")  # help_text="This should be checkmarked...
    value = models.IntegerField("Office Points", help_text="This is how much it contributes to the Office Leaderboard")
    datetime = models.DateTimeField("Start Date & Time")
    players = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = HTMLField("War Description", max_length=1000, null=True, default="No Description")
    # players = models.ForeignKey(Player)
    playerPoints = models.IntegerField(null=True)

# class PlayerSearch(models.Model):
#
#     querylist = User.objects.all()[:10]
#     player_list = models.ForeignKey(choices=querylist)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    war = models.ForeignKey(War, on_delete=models.CASCADE)
    warpoints = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User)
    profilePicture = models.FileField(upload_to='uploads/')


class Tournament(models.Model):
    type = models.CharField(max_length=100)
    players = []


class Bracket(models.Model):
    tournament = models.ForeignKey(Tournament)
    players = models.ForeignKey(User)
    min_size = models.IntegerField()
    bracket_type = models.CharField(max_length=100)

# class Player(models.Model):
#     player_name = models.CharField(max_length=100)
