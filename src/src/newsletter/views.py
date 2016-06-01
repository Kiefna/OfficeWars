import sys
from django.contrib.auth.decorators import login_required
from random import shuffle
from django.conf import settings
from django.core.mail import send_mail
from django.core.serializers import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile, Tournament
from django.template.context_processors import csrf
from django.contrib.admin.options import IS_POPUP_VAR
from ajax_select.fields import autoselect_fields_check_can_add

from .forms import ContactForm, SignUpForm, PlayerForm, WarForm, PlayerSearch
from .models import SignUp, War

playerlist = []
matchups = []
mixedlist = []
teams = {}
teamNames = ["Victorious Secret", "Second Worst Team at the Table",
             "Holla Koalas", "Designated Drinkers",
             "Natural Born Drinkers", "To Infinity and Beerpong",
             "Smarty Pints", "The Donald Drunks", "King Pong", "Vomiteers",
             "Drunken Masters", "Hillary 'Pint'on", "Beernie Sanders",
             "License to Pong", "Live and Let Pong",
             "Game of Pongs", "Beerack Oponga", "Beer Pressure", "It's Over When We're Sober", "Brewlius Caesar"]


# Create your views here.

def contact(request):
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        # 	print key, value
        # 	#print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'youotheremail@email.com']
        contact_message = "%s: %s via %s" % (
            form_full_name,
            form_message,
            form_email)
        some_html_message = """<h1>hello</h1>"""
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  html_message=some_html_message,
                  fail_silently=True)

    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "forms.html", context)


def sort(request):
    title = "Sort Players"
    shuffle(playerlist)
    shuffle(teamNames)
    print playerlist

    j = 0
    for name in playerlist:
        if name == "":
            playerlist.pop(j)
        if (name == "clear") or (name == "Clear"):
            global playerlist
            playerlist = []
            global matchups
            matchups = []
            global mixedlist
            mixedlist = []
            global teams
            teams = {}
            return render(request, "home.html")

        j += 1

    print len(playerlist)

    if ((len(playerlist) % 2) == 0) and (len(playerlist) > 3):

        l = 0
        playeriterator = iter(playerlist)
        for player in playeriterator:
            teams[teamNames[l]] = (player, next(playeriterator))
            l += 1

        teamiterator = iter(teams)
        for team in teamiterator:
            matchups.append((team, next(teamiterator)))

        # print matchups
        # print teams
        # print playerlist

        for match in matchups:
            for team in match:
                players = teams[team]
                print players
                mixedlist.append(players[0])
                mixedlist.append(players[1])

    context = {
        "playerList": playerlist,
        "teams": teams,
        "matchups": matchups,
        "mixedlist": mixedlist,
        "error": "oddNum",
    }

    if (len(matchups) % 2) == 1:
        global playerlist
        playerlist = []
        global matchups
        matchups = []
        global mixedlist
        mixedlist = []
        global teams
        teams = {}

        context = {
            "playerList": playerlist,
            "teams": teams,
            "matchups": matchups,
            "mixedlist": mixedlist,
            "error": "oddNumMatchups",
        }

        return render(request, "error.html", context)

    if (len(playerlist) % 2) == 1:
        global playerlist
        playerlist = []
        global matchups
        matchups = []
        global mixedlist
        mixedlist = []
        global teams
        teams = {}

        context = {
            "playerList": playerlist,
            "teams": teams,
            "matchups": matchups,
            "mixedlist": mixedlist,
            "error": "oddNumPlayers",
        }

        return render(request, "error.html", context)

    if len(playerlist) < 4:
        global playerlist
        playerlist = []
        global matchups
        matchups = []
        global mixedlist
        mixedlist = []
        global teams
        teams = {}

        context = {
            "playerList": playerlist,
            "teams": teams,
            "matchups": matchups,
            "mixedlist": mixedlist,
            "error": "tooFew",
        }

        return render(request, "error.html", context)

    return render(request, "sort.html", context)


def create(request):
    title1 = "Add players"
    form = PlayerForm(request.POST)
    if form.is_valid():
        form_playername = form.cleaned_data.get("player_name")
        if form_playername not in playerlist:
            playerlist.append(form_playername)

    context = {
        "form": form,
        "playerList": playerlist,
    }
    return render(request, "create.html", context)


def home(request):
    title = 'Sign Up Now'
    form = SignUpForm(request.POST or None)
    context = {
        "title": title,
        "form": form
    }

    if form.is_valid():
        # form.save()
        # print request.POST['email'] #not recommended
        instance = form.save(commit=False)

        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "New full name"
        instance.full_name = full_name
        # if not instance.full_name:
        # 	instance.full_name = "Justin"
        instance.save()
        context = {
            "title": "Thank you"
        }

    if request.user.is_authenticated() and request.user.is_staff:
        # print(SignUp.objects.all())
        # i = 1
        # for instance in SignUp.objects.all():
        # 	print(i)
        # 	print(instance.full_name)
        # 	i += 1

        queryset = SignUp.objects.all().order_by('-timestamp')  # .filter(full_name__iexact="Justin")
        # print(SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="Justin").count())
        context = {
            "queryset": queryset
        }

    return render(request, "home.html", context)


def war_main(request):
    title = 'Create a War'
    form = WarForm(request.POST or None)
    context = {
        "title": title,
        "form": form
    }

    if not request.user.is_anonymous():
        if form.is_valid():
            # form.save()
            # print request.POST['email'] #not recommended
            instance = form.save(commit=False)

            # Extraneous useless meddling - Fidgeting
            war_name = form.cleaned_data.get("war_name")
            description = form.cleaned_data.get("description")
            print description
            i = 0
            war_name = war_name.replace(" ", "-")
            print war_name
            if not war_name:
                war_name = "Choose a new War title"
            instance.players = request.user
            instance.war_name = war_name
            war_type = instance.war_type
            # if instance.description:
            #     instance.description = "No Description"

            # if not instance.full_name:
            # 	instance.full_name = "Justin"
            instance.save()

            a = UserProfile(user=request.user, war=instance, warpoints=0)
            a.save()

            # b = Tournament(type=instance.war_type)

            context = {
                "title": title,
                "form": form,
                "war_name": war_name,
                "war_type": war_type,
            }

            # queryset = War.objects.all().order_by('datetime')
            # for item in queryset:
            #     print item.war_name
            #     print item.war_type

            # queryset2 = User.objects.all()
            # for item2 in queryset2:
            #     print item2.username

            return HttpResponseRedirect('/war_list/')
    else:
        return HttpResponseRedirect('/accounts/register/')

    return render(request, "war_create.html", context)


def war_list(request):
    # print request.user
    if request.user.is_anonymous():
        # print "aloha"
        title = "Current Wars"
        queryset = War.objects.all().order_by('datetime')[:30]
        context = {
            "title": title,
            "queryset": queryset,
            "currentuser": request.user,
        }

        return render(request, "about.html", context)

    else:
        title = "Your Wars"
        queryset = War.objects.all().order_by('datetime').filter(players=request.user)
        queryset2 = UserProfile.objects.filter(user=request.user)
        # print queryset
        # print queryset2
        # for item in queryset:
        #     for item2 in queryset2:
        #         if item.players == item2.user:
        #             queryset2.remove(item2)

        # print"----------"
        # print"----------"

        context = {
            "title": title,
            "queryset": queryset,
            "queryset2": queryset2,
            "currentuser": request.user,
        }

        return render(request, "about.html", context)


def war_view(request, war_name, user="default", vote="default"):

    if (request.method == "GET") and ((user != "default") and (vote == "up")):
        wartemp2 = War.objects.filter(war_name=war_name)
        for item in wartemp2[0].userprofile_set.all():
            if str(item.user) == user:
                item.warpoints += 1
                item.save()

    if (request.method == "GET") and ((user != "default") and (vote == "down")):
        wartemp2 = War.objects.filter(war_name=war_name)
        for item in wartemp2[0].userprofile_set.all():
            if str(item.user) == user:
                item.warpoints -= 1
                item.save()

    for item in request.POST:
        print item

    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/register/')

    if request.POST.get('points', False):
        print request.POST["points"]

    if request.POST:
        if not request.POST.get('points', False):
            newplayer = request.POST["username"]
            # print newplayer
            # print request.user
            # print "weird"
            if request.POST["username"]:
                # print User.objects.filter(username=newplayer)
                playertemp = User.objects.filter(username=newplayer)
                wartemp = War.objects.filter(war_name=war_name).filter(players=request.user)
                # print wartemp
                # print wartemp[0]
                # print wartemp[0].war_name
                # print "----------"
                # print wartemp[0].userprofile_set.all()
                flag = True
                for object in wartemp[0].userprofile_set.all():
                    if object.user == playertemp[0]:
                        flag = False

                if flag:
                    a = UserProfile(user=playertemp[0], war=wartemp[0], warpoints=0)
                    a.save()
                    # print "------------"
                    # print a.user
                    # print a.war.war_name

    try:
        # print "trying"
        form = PlayerSearch(request.POST or None)
        wartemp = War.objects.filter(war_name=war_name)

        if wartemp[0]:
            # print "still trying"
            if wartemp[0].userprofile_set:
                queryset = War.objects.all().filter(war_name=war_name)
                for item in queryset:
                    if item.war_name == war_name:
                        war = item

            if wartemp[0].get_war_type_display() == "Leaderboard":

                warLeaderboardList = []
                for player in wartemp[0].userprofile_set.all():
                    warLeaderboardList.append(player)

                warLeaderboardList.append(war.players)

            blanklist = []
            x = 0
            while (x < len(wartemp[0].userprofile_set.all()) - 1) and (x < 3):
                print "blanklist:" + str(x)
                blanklist.append([])
                x += 1

        context = {
            "war": war,
            "form": form,
            "players": wartemp[0].userprofile_set.all().order_by('-warpoints'),
            "currentuser": request.user,
            "blanklist": blanklist,
        }

        return render(request, "war_view.html", context)  # def war_edit():

    except UnboundLocalError:
        # safety catch
        print "HUH!!!"

        form = PlayerSearch(request.POST or None)

        # autoselect_fields_check_can_add(form, User, request.user)

        if request.user.is_anonymous():
            title = "Please Log In"
            context = {
                "title": title,
            }

            return render(request, "war_view.html", context)

        else:
            queryset = War.objects.all().order_by('datetime').filter(players=request.user)[:30]
            for item in queryset:
                if item.war_name == war_name:
                    war = item

            context = {
                "war": war,
                "form": form,
                "currentuser": request.user,
            }

            return render(request, "war_view.html", context)  # def war_edit():  # return render()

# @login_required
# def like_category(request):
#     context = RequestContext(request)
#     point_id = None
#     if request.method == 'GET':
#         point_id = request.GET['category_id']
#
#     likes = 0
#     if cat_id:
#         category = Category.objects.get(id=int(point_id))
#         if category:
#             likes = category.likes + 1
#         category.likes = likes
#         category.save()
#
#     return HttpResponse(likes)
