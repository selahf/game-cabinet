from django.shortcuts import render
from .models import Game


def game_list(request):
    games = Game.objects.all()
    return render(request, "home.html", {"games": games})
