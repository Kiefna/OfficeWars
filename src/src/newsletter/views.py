import sys
from django.contrib.auth.decorators import login_required
from random import shuffle
from django.conf import settings
from django.core.mail import send_mail
from django.core.serializers import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile, Bracket, Office
from django.template.context_processors import csrf
from django.contrib.admin.options import IS_POPUP_VAR
from ajax_select.fields import autoselect_fields_check_can_add
from django.contrib.auth.decorators import login_required
from django.template import Context

from .forms import ContactForm, SignUpForm, PlayerForm, WarForm, PlayerSearch, UserProfileUpdateForm1, \
    UserProfileUpdateForm2, UserProfileUpdateForm3, OfficeCreate, OfficeSearch, ChatForm
from .models import SignUp, War, Profile, Room

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

    form = ChatForm(request.POST)
    rooms = Room.objects.order_by("title")
    # if request.POST:
    #     if form.is_valid():
    context = {
        "form": form,
        "rooms": rooms
    }


    # title = 'Sign Up Now'
    # form = SignUpForm(request.POST or None)
    # context = {
    #     "title": title,
    #     "form": form
    # }
    #
    # if form.is_valid():
    #     # form.save()
    #     # print request.POST['email'] #not recommended
    #     instance = form.save(commit=False)
    #
    #     full_name = form.cleaned_data.get("full_name")
    #     if not full_name:
    #         full_name = "New full name"
    #     instance.full_name = full_name
    #     # if not instance.full_name:
    #     # 	instance.full_name = "Justin"
    #     instance.save()
    #     context = {
    #         "title": "Thank you"
    #     }
    #
    # if request.user.is_authenticated() and request.user.is_staff:
    #     # print(SignUp.objects.all())
    #     # i = 1
    #     # for instance in SignUp.objects.all():
    #     # 	print(i)
    #     # 	print(instance.full_name)
    #     # 	i += 1
    #
    #     queryset = SignUp.objects.all().order_by('-timestamp')  # .filter(full_name__iexact="Justin")
    #     # print(SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="Justin").count())
    #     context = {
    #         "queryset": queryset
    #     }

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
            # print request.POST['email'] # not recommended
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

            b = Bracket(tournament=instance, players=instance.players, bracket_row="base")
            b.save()

            print "###############"
            print b
            print b.players
            print b.tournament.war_name
            print "###############"

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
        queryset = War.objects.order_by('datetime')[:30]
        context = {
            "title": title,
            "queryset": queryset,
            "currentuser": request.user,
        }

        return render(request, "about.html", context)

    else:
        title = "Your Wars"
        queryset = War.objects.order_by('datetime').filter(players=request.user)
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


def war_view(request, war_name, user="default", vote="default", loss="False"):

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
                for object2 in wartemp[0].userprofile_set.all():
                    if playertemp:
                        if object2.user == playertemp[0]:
                            flag = False
                    else:
                        flag = False


                if flag:
                    a = UserProfile(user=playertemp[0], war=wartemp[0], warpoints=0)
                    a.save()
                    b = Bracket(players=playertemp[0], tournament=wartemp[0], bracket_row="base")
                    b.save()
                    return HttpResponseRedirect('')
                    # print "------------"
                    # print a.user
                    # print a.war.war_name

    if (request.method == "GET") and ((user != "default") and (vote == "True")):
        current_user = User.objects.filter(username=user)
        current_war = War.objects.filter(war_name=war_name)
        current_bracket = Bracket.objects.filter(players=current_user, tournament=current_war)
        # current_bracket[0].delete()
        bracket2 = current_bracket[0]
        bracket2.bracket_type = "LOSS"
        bracket2.save()

        counter = 0
        for bracket in Bracket.objects.filter(tournament=current_war):

            if bracket.bracket_type == "LOSS":
                counter += 1

        # if (len(current_war[0].userprofile_set.all()) % 2) == 0:
        #     print (len(current_war[0].userprofile_set.all()) / 4)
        #     print len(Bracket.objects.filter(tournament=current_war))
        #     if len(Bracket.objects.filter(tournament=current_war)) == (
        #                 len(current_war[0].userprofile_set.all()) / 2):
        #         if counter == 2:
        #             print "coconut"
        #             for bracket3 in Bracket.objects.filter(tournament=current_war):
        #                 if bracket3.bracket_type == "LOSS":
        #                     bracket3.delete()

        if (len(current_war[0].bracket_set.all()) % 2) == 0:
            if counter >= (len(current_war[0].bracket_set.all()) / 2):
                for bracket2 in Bracket.objects.filter(tournament=current_war):
                    if bracket2.bracket_type == "LOSS":
                        bracket2.delete()

        else:
            if counter == ((len(current_war[0].bracket_set.all()) - 1) / 2):
                for bracket2 in Bracket.objects.filter(tournament=current_war):
                    if bracket2.bracket_type == "LOSS":
                        bracket2.delete()

    try:
        # print "trying"
        form = PlayerSearch(request.POST or None, initial={"username": ""})
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

            if wartemp[0].get_war_type_display() == "Tournament":
                pairs = []
                currentPlayers = []
                currentBracketList = []
                for bracket in wartemp[0].bracket_set.all():
                    if bracket.bracket_row == "base":
                        currentPlayers.append(bracket.players)
                        currentBracketList.append(bracket)

                if len(currentPlayers) % 2 == 0:
                    playerit = iter(currentPlayers)
                    for player in playerit:
                        pairs.append([player, playerit.next()])

                else:
                    playerit = iter(currentPlayers)

                    for player in playerit:
                        try:
                            pairs.append([player, playerit.next()])
                        except IndexError:
                            print "Error"
                            pairs.append([player])
                        except StopIteration:
                            print "Error2"
                            pairs.append([player])

                            # print "bracket: " + str(bracket)
                            # print bracket.players
                            # if bracket.bracket_row == "base":
                            #     print "wowowowow"
                            #     bracketBase = bracket
                            #
                            #     if isinstance(bracketBase.players, User):
                            #         continue
                            #
                            #     elif len(bracketBase.players) % 2 == 0:
                            #         playerit = iter(bracket.players)
                            #         for player in playerit:
                            #             pairs.append([player, playerit.next()])
                            #
                            #     else:
                            #
                            #         playerit = iter(bracket.players)
                            #
                            #         for player in playerit:
                            #             try:
                            #                 pairs.append([player, playerit.next()])
                            #             except IndexError:
                            #                 print "Error"
                            #                 pairs.append([player])
                            #
                            # else:
                            #     pairs = []

                blanklist = []
                x = 0
                while (x < len(wartemp[0].userprofile_set.all()) - 1) and (x < 3):
                    print "blanklist:" + str(x)
                    blanklist.append([])
                    x += 1

                # if isinstance(bracketBase.players, User):
                #     currentPlayers = [bracketBase.players]
                # else:
                #     currentPlayers = bracketBase.players

                context = {
                    "war": war,
                    "form": form,
                    "players": wartemp[0].userprofile_set.all().order_by('-warpoints'),
                    "currentuser": request.user,
                    "blanklist": blanklist,
                    "currentBracket": pairs,
                    "currentPlayers": currentPlayers,
                    "currentBracketList": currentBracketList,
                }

                return render(request, "war_view.html", context)

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


@login_required()
def profile(request):
    print "+++++++++++"
    print request.user.user.title
    print request.user.user.description

    title = 'Profile'

    form1 = UserProfileUpdateForm1(request.POST or None, initial={'email': request.user.email})
    form2 = UserProfileUpdateForm2(request.POST or None,
                                   initial={'title': request.user.user.title,
                                            'description': request.user.user.description})
    form3 = UserProfileUpdateForm3(request.POST or None, request.FILES,
                                   initial={'profilePicture': request.user.user.profilePicture})

    # initial={'title': request.user.user.title,
    #                                'description': request.user.user.description})
    # request.FILES)

    context = {
        "title": title,
        "form1": form1,
        "form2": form2,
        "form3": form3
    }

    if request.user.is_authenticated():

        if request.method == "POST":

            if form1.is_valid():

                if form2.is_valid():

                    if form3.is_valid():
                        # instance2 = form2.save(commit=False)
                        # # # form.save()
                        # # # print request.POST['email'] # not recommended
                        # instance1 = form1.save(commit=False)
                        # Extraneous useless meddling - Fidgeting
                        # war_name = form.cleaned_data.get("war_name")
                        # description = form.cleaned_data.get("description")

                        # instance.players = request.user
                        # instance.war_name = war_name
                        # war_type = instance.war_type
                        # if instance.description:
                        #     instance.description = "No Description"

                        # if not instance.full_name:
                        # 	instance.full_name = "Justin"
                        # print "--------------"
                        # print instance1.email
                        # # print instance2.user
                        # print instance2.profilePicture
                        # print instance2.title
                        # print instance2.description
                        # print "--------------"
                        #
                        # instance1.save()
                        # instance2.save()

                        currentUser = request.user

                        tempPhoto = form3.cleaned_data.get("profilePicture")
                        print "***" + str(tempPhoto) + "***"
                        if not tempPhoto == "../static/img/Bot.png":
                            currentUser.user.profilePicture = tempPhoto
                        # print "*"
                        # print currentUser.user.profilePicture
                        # print "*"
                        tempTitle = form2.cleaned_data.get("title")
                        if tempTitle:
                            currentUser.user.title = tempTitle
                        # print currentUser.user.title
                        tempDescription = form2.cleaned_data.get("description")
                        if tempDescription:
                            currentUser.user.description = tempDescription
                        # print currentUser.user.description
                        tempEmail = form1.cleaned_data.get("email")

                        if tempEmail:
                            currentUser.email = tempEmail

                        currentUser.user.save()
                        currentUser.save()
                        # print "*2"
                        # print currentUser.user.profilePicture
                        # print "*2"
                        # a = UserProfile(user=request.user, war=instance, warpoints=0)
                        # a.save()
                        #
                        # b = Bracket(tournament=instance, players=instance.players, bracket_row="base")
                        # b.save()

                        context = {
                            "title": title,
                            "form1": form1,
                            "form2": form2,
                            "form3": form3
                        }
                        return HttpResponseRedirect('/profile/')

                        # else:
                        #     form = ContactForm(
                        #         initial={'subject': 'I love your site!'}
                        #     )

    return render(request, "profile.html", context)


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

@login_required()
def officeCreate(request):
    title = 'Office Create'

    form = OfficeCreate(request.POST or None, request.FILES)

    # initial={'title': request.user.user.title,
    #                                'description': request.user.user.description})
    # request.FILES)

    context = {
        "title": title,
        "form": form
    }

    if request.user.is_authenticated():

        if request.method == "POST":

            if form.is_valid():

                if request.user.user.office:
                    # print "has OFFICE!!!!!"

                    # instance2 = form2.save(commit=False)
                    # # # form.save()
                    # # # print request.POST['email'] # not recommended
                    # instance1 = form1.save(commit=False)
                    # Extraneous useless meddling - Fidgeting
                    # war_name = form.cleaned_data.get("war_name")
                    # description = form.cleaned_data.get("description")

                    # instance.players = request.user
                    # instance.war_name = war_name
                    # war_type = instance.war_type
                    # if instance.description:
                    #     instance.description = "No Description"

                    # if not instance.full_name:
                    # 	instance.full_name = "Justin"
                    # print "--------------"
                    # print instance1.email
                    # # print instance2.user
                    # print instance2.profilePicture
                    # print instance2.title
                    # print instance2.description
                    # print "--------------"
                    #
                    # instance1.save()
                    # instance2.save()
                    tempOfficeName = form.cleaned_data.get("officeName")
                    if tempOfficeName:
                        if request.user.user.office:
                            request.user.user.office.officeName = tempOfficeName

                    # currentUser = request.user
                    # Office.objects.all().filter(officeName="tempOfficeName")
                    if request.user.user.office:
                        tempOfficeShield = form.cleaned_data.get("officeShield")
                        print tempOfficeShield
                        if not tempOfficeShield == "../static/img/Bot.png":
                            request.user.user.office.officeShield = tempOfficeShield

                        tempOfficeDescription = form.cleaned_data.get("officeDescription")
                        print tempOfficeDescription
                        if tempOfficeDescription:
                            request.user.user.office.officeDescription = tempOfficeDescription

                        tempOfficeType = form.cleaned_data.get("officeType")
                        if tempOfficeType:
                            request.user.user.office.officeType = tempOfficeDescription

                        tempOfficeSize = form.cleaned_data.get("officeSize")
                        if tempOfficeSize:
                            request.user.user.office.officeSize = tempOfficeSize

                        print tempOfficeName
                        print tempOfficeSize
                        print tempOfficeDescription
                        print tempOfficeShield

                else:
                    tempOfficeName = form.cleaned_data.get("officeName")
                    tempOfficeType = form.cleaned_data.get("officeType")
                    tempOfficeSize = form.cleaned_data.get("officeSize")
                    tempOfficeDescription = form.cleaned_data.get("officeDescription")
                    tempOfficeShield = form.cleaned_data.get("officeShield")
                    o = Office(officeName=tempOfficeName, officeType=tempOfficeType, officeSize=tempOfficeSize,
                               officeDescription=tempOfficeDescription, officeShield=tempOfficeShield)
                    o.save()
                    request.user.user.office = o
                    request.user.user.save()

                    print tempOfficeName
                    print tempOfficeSize
                    print tempOfficeDescription
                    print tempOfficeType
                    print tempOfficeShield

                    query = Office.objects.all()
                    for item in query:
                        print item.officeName

                request.user.user.rank = "LD"
                request.user.user.save()
                return HttpResponseRedirect('/')

                # else:
                #     form = ContactForm(
                #         initial={'subject': 'I love your site!'}
                #     )

    return render(request, "officeCreate.html", context)


@login_required()
def officeView(request, slug="blank", join=False):
    if request.user.user.office:
        query = request.user.user.office.profile_set.all()
    else:
        query = {}

    query2 = Office.objects.filter(slug=slug)

    if join:
        if not request.user.user.office:
            request.user.user.office = query2[0]
            request.user.user.save()
            return HttpResponseRedirect('officeView')

    # print query2

    if query2:

        query3 = query2[0].profile_set.all()
        context = {
            "office_name": query2[0].officeName,
            "query": query,
            "query2": query2[0],
            "query3": query3
        }

    elif slug == "blank":

        context = {
            "office_name": slug,
            "query": query,
        }

    else:
        context = {
            "office_name": "error404",
            "query": query,
        }

    return render(request, "officeView.html", context)


@login_required()
def searchView(request):
    form = OfficeSearch(request.POST or None)

    query = Office.objects.all()
    for item in query:
        print item.slug
    context = {
        "form": form,
        "query": query
    }
    # print "request"
    # print request
    # print "working"
    return render(request, "officeSearchResult.html", context)

    # query = request.GET
    # for item in query:
    #     print hello
    #     print item
    # c = Context({'query': query})
    # return render(request, " ", c)
    # return render(request, " ", c)


def navbarSearchView(request):
    return TemplateResponse(request, "yourtemplate.html", {'form': OfficeSearch()})
