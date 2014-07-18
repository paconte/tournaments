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
        print(game)
        print(game.phase)
        print(game.phase.round)
        print(GameRound.LIGA)
        if game.phase.round == GameRound.LIGA:
            liga_games.append(game)
        elif (game.phase.round == GameRound.POOL_A 
              or game.phase.round == GameRound.POOL_B        
              or game.phase.round == GameRound.POOL_C
              or game.phase.round == GameRound.POOL_D):
            pool_games.append(game)
        else:
            playoffs_games.append(game)
            print playoffs_games       

    return render(request, 
                  'tournaments/detail_tournament.html', 
                  {'tournament_list': tournament_list, 'tournament': tournament, 'games': games, 'liga_games': liga_games, 'pool_games': pool_games, 'playoffs_games': playoffs_games,})


def detail_team(request, tournament_id, team_id):
    tournament_list = Tournament.objects.all()
    #team = Team.objects.get(pk=team_id)
    team = get_object_or_404(Team, pk=team_id)
    games = Game.objects.filter(Q(tournament=tournament_id), Q(local=team_id) | Q(visitor=team_id))
    players = Player.objects.filter(team=team_id)
    return render(request, 'tournaments/detail_team.html', {'team': team, 'games': games, 'players': players, 'tournament_list': tournament_list,})

class ClassificationRow:
    plus = 0
    minus = 0
    plus_minus = 0
    
    def __init__(self, team_name):
        self.team_name = team_name

    def __eq__(self, other):
        self.team_name == other.team_name          
                
    
class Fixtures:
    liga_games = []
    pool_games = []
    playoff_games = []

    liga_clasification = []
    liga_winners = []
    liga_losers = []
    liga_draws = []

    def __init__(self, games):
        for game in games:
            if game.phase.round == GameRound.LIGA:
                self.liga_games.append(game)
            elif (game.phase.round == GameRound.POOL_A 
                  or game.phase.round == GameRound.POOL_B        
                  or game.phase.round == GameRound.POOL_C
                  or game.phase.round == GameRound.POOL_D):
                self.pool_games.append(game)
            else:
                self.playoffs_games.append(game)
                
        for game in liga_games:
            if game.local_score > game.visitor_score:
                liga_winners.append(game.local)
                liga_losers.append(game.visitor)
            elif game.local_score < game.visitor_score:
                liga_winners.append(game.visitor)
                liga_losers.append(game.local)
            else:
                liga_draws.append(game.local)
                liga_draws.append(game.visitor)
                
        for game in pool_games:
            if game.local_score > game.visitor_score:
                pool_winners.append(game.local)
                pool_losers.append(game.visitor)
            elif game.local_score < game.visitor_score:
                pool_winners.append(game.visitor)
                pool_losers.append(game.local)
            else:
                pool_draws.append(game.local)
                pool_draws.append(game.visitor)

#    def get_won_games(team):
        
