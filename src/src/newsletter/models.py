from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.conf import settings
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from registration.signals import user_registered
from django.template.defaultfilters import slugify


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
    value = models.IntegerField("Office Points", help_text="This is how much it contributes to the Office Leaderboard",
                                null=True)
    datetime = models.DateTimeField("Start Date & Time")
    players = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = HTMLField("War Description", max_length=1000, null=True, default="No Description")
    # players = models.ForeignKey(Player)
    playerPoints = models.IntegerField(null=True)


# class PlayerSearch(models.Model):
#
#     querylist = User.objects.all()[:10]
#     player_list = models.ForeignKey(choices=querylist)

class Office(models.Model):
    LARGEOFFICE = 'LO'
    MEDIUMOFFICE = 'MO'
    SMALLOFFICE = 'SO'

    OFFICESIZE_CHOICES = (
        (LARGEOFFICE, "Large Office - (50+ employees)"),
        (MEDIUMOFFICE, "Medium Office - (20 - 49 employees)"),
        (SMALLOFFICE, "Small Office - (2 - 19 employees)"),
    )

    officeName = models.CharField(max_length=100)
    officeSize = models.CharField(max_length=2, choices=OFFICESIZE_CHOICES, default=SMALLOFFICE, null=True)
    officeType = models.CharField(
        max_length=100,
        null=True)  # Add a option that allows people to add new types of Offices but make it a choice field
    officeDescription = models.TextField(max_length=500, null=True, blank=True)
    officeShield = models.ImageField(upload_to='profilePictures', null=True,
                                     default='../static/img/QuestionShield.png'
                                     )
    slug = models.SlugField()  # unique=True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.officeName)

        print "---------"
        print self.slug
        print "---------"
        super(Office, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.officeName
    # officeProfiles = models.ForeignKey(OfficeProfiles)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    war = models.ForeignKey(War, on_delete=models.CASCADE)
    warpoints = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user')

    profilePicture = models.ImageField(upload_to='profilePictures', null=True,
                                       default='../static/img/Bot.png'
                                       )
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    office = models.ForeignKey(Office, null=True)


# def assure_user_profile_exists(pk):
#     """
#     Creates a user profile if a User exists, but the
#     profile does not exist.  Use this in views or other
#     places where you don't have the user object but have the pk.
#     """
#     user = User.objects.get(pk=pk)
#     try:
#         # fails if it doesn't exist
#         userprofile = user.userprofile
#     except UserProfile.DoesNotExist, e:
#         userprofile = UserProfile(user=user)
#         userprofile.save()
#     return

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class Bracket(models.Model):
    tournament = models.ForeignKey(War)
    players = models.ForeignKey(User)
    min_size = models.IntegerField(null=True)
    bracket_type = models.CharField(max_length=100, null=True)
    bracket_row = models.CharField(max_length=100)

# class Player(models.Model):
#     player_name = models.CharField(max_length=100)
