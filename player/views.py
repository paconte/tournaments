from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from player.models import Tournament
from player.models import Game

# Create your views here.
def index(request):
    tournament_list = Tournament.objects.all()
    template = loader.get_template('tournaments/index.html')
    context  = RequestContext(request, {'tournament_list': tournament_list, })
    return HttpResponse(template.render(context))

def detail(request, tournament_id):
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
        games = Game.objects.filter(tournament=tournament_id)
    except Tournament.DoesNotExist:
        raise Http404
    return render(request, 'tournaments/detail.html', {'tournament': tournament, 'games': games})

def detail_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    return render(request, 'tournaments/detail.html', {'team': team})
