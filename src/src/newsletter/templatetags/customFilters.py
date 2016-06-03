import sys
from django import template
from django.template.defaultfilters import stringfilter
import random

register = template.Library()


@register.filter(name="leader")
def leader(war):
    queryset = war.userprofile_set.all().order_by('-warpoints')
    return queryset[0].user


@register.filter(name="pair")
def pair(players):
    pairs = []

    playerit = iter(players)
    if len(players) % 2 == 0:
        for player in playerit:
            pairs.append([player, playerit.next()])
    else:
        return pairs
    return pairs


@register.filter(name="shuffle")
def shuffle(players):
    playerlist = []

    for item in players:
        if item != "None":
            print item
            print "-----------"
            playerlist.append(item.user)
            print playerlist

    newlist = random.sample(playerlist, len(playerlist))
    print newlist
    return newlist

# @register.filter(name="getBracket")
# def getBracket(player):
#     player.
#     return newlist