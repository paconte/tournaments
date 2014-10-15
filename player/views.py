from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
from django.shortcuts import get_object_or_404

from player.models import Tournament
from player.models import Game
from player.models import GameRound
from player.models import Team
from player.models import Player
from player.models import PlayerStadistic

from django.views.generic import DetailView

from service import *

# Create your views here.
def index(request):
    tournament_list = Tournament.objects.all()
    template = loader.get_template('tournaments/index.html')
    context  = RequestContext(request, {'tournament_list': tournament_list, })
    return HttpResponse(template.render(context))

def detail_tournament(request, tournament_id):
    tournament_list = Tournament.objects.all()
    try:
        tournament = Tournament.objects.get(pk=tournament_id)
        games = Game.objects.filter(tournament=tournament_id)
    except Tournament.DoesNotExist:
        raise Http404
    
    liga_games = [] 
    pool_games = []
    playoffs_games = []

    for game in games:
        if game.phase.round == GameRound.LIGA:
            liga_games.append(game)
        elif (game.phase.round == GameRound.POOL_A 
              or game.phase.round == GameRound.POOL_B        
              or game.phase.round == GameRound.POOL_C
              or game.phase.round == GameRound.POOL_D):
            pool_games.append(game)        
        else:
            playoffs_games.append(game)
    
    fixtures = Fixtures(games)
    fixtures.sort_pools()
    teams = Team.objects.filter(tournament__id=tournament_id)
    teams_matrix = TeamsMatrix(3, teams)
    st_utils = StructuresUtils()

    return render(request, 
                  'tournaments/detail_tournament.html', 
                  {'tournament_list': tournament_list, 
                   'tournament': tournament, 
                   'games': games, 
#                   'liga_games': liga_games, 
                   'sorted_pools': fixtures.sorted_pools, 
#                   'pool_games': fixtures.pool_games, 
#                   'playoffs_games': playoffs_games, 
#                   'fixtures': fixtures, 
                   'finals':fixtures.get_finals({}), 
#                   'teams_matrix': teams_matrix.matrix, })
                   'teams_matrix': st_utils.get_teams_matrix(teams, 4), })

def detail_team(request, tournament_id, team_id):
    tournament_list = Tournament.objects.all()
    tournament = Tournament.objects.get(pk=tournament_id)
    #team = Team.objects.get(pk=team_id)
    team = get_object_or_404(Team, pk=team_id)
    games = Game.objects.filter(Q(tournament=tournament_id), Q(local=team_id) | Q(visitor=team_id))    
    players = Player.objects.filter(team=team_id)
    stadistics = []
    for player in players:
        stadistics.extend(PlayerStadistic.objects.filter(player=player.id))
    st_utils = StructuresUtils()

    return render(request, 'tournaments/detail_team.html', 
                  {'team': team, 
                   'games': st_utils.get_team_view_games(games), 
                   'players': st_utils.get_team_details_matrix(stadistics, players), 
                   'tournament_list': tournament_list,
                   'tournament': tournament, })

def detail_game(request, tournament_id, game_id):
    tournament_list = Tournament.objects.all()
    game = Game.objects.filter(pk=game_id)
    stadistics = PlayerStadistic.objects.filter(game=game_id)
    local_players = Player.objects.filter(team=game[0].local)
    visitor_players = Player.objects.filter(team=game[0].visitor)
    st_utils = StructuresUtils()
    st_utils.get_game_details_matrix(stadistics, local_players, visitor_players)

    return render(request, 'tournaments/detail_game.html',
                  {'game': game[0],
                   'stadistics': st_utils.get_game_details_matrix(stadistics, local_players, visitor_players),
                   'tournament_list': tournament_list, })
