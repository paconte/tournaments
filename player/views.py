from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
from django.shortcuts import get_object_or_404

from player.models import Tournament
from player.models import Game
from player.models import Team
from player.models import Player

# Create your views here.
def index(request):
    tournament_list = Tournament.objects.all()
    template = loader.get_template('tournaments/index.html')
    context  = RequestContext(request, {'tournament_list': tournament_list, })
    return HttpResponse(template.render(context))

def detail_tournament(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
        games = Game.objects.filter(tournament=tournament_id)
    except Tournament.DoesNotExist:
        raise Http404
    return render(request, 'tournaments/detail_tournament.html', {'tournament': tournament, 'games': games})


def detail_team(request, tournament_id, team_id):
    #team = Team.objects.get(pk=team_id)
    team = get_object_or_404(Team, pk=team_id)
    games = Game.objects.filter(Q(tournament=tournament_id), Q(local=team_id) | Q(visitor=team_id))
    players = Player.objects.filter(team=team_id)
    return render(request, 'tournaments/detail_team.html', {'team': team, 'games': games, 'players': players})
