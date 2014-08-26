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

from operator import attrgetter

import re

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
#        print(game)
#        print(game.phase)
#        print(game.phase.round)
#        print(GameRound.LIGA)
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
    
    fixtures = Fixtures(games)
    fixtures.sort_pools()
    print(fixtures.get_games(games, GameRound.POOL_A, []))
    #print(games)
    #print(fixtures.pool_rows)    
    #print(fixtures.sorted_pools)
    #print(fixtures.get_sorted_pools)
    teams = Team.objects.filter(tournament__id=tournament_id)
   
    return render(request, 
                  'tournaments/detail_tournament.html', 
                  {'tournament_list': tournament_list, 'tournament': tournament, 'games': games, 'liga_games': liga_games, 'sorted_pools': fixtures.sorted_pools, 'pool_games': fixtures.pool_games, 'playoffs_games': playoffs_games, 'fixtures': fixtures, })


def detail_team(request, tournament_id, team_id):
    tournament_list = Tournament.objects.all()
    #team = Team.objects.get(pk=team_id)
    team = get_object_or_404(Team, pk=team_id)
    games = Game.objects.filter(Q(tournament=tournament_id), Q(local=team_id) | Q(visitor=team_id))
    players = Player.objects.filter(team=team_id)
    return render(request, 'tournaments/detail_team.html', {'team': team, 'games': games, 'players': players, 'tournament_list': tournament_list,})

class ClassificationRow:    
    played = 0
    won = 0
    lost = 0
    drawn = 0
    plus = 0
    minus = 0
    plus_minus = 0
    points = 0

    def __repr__(self):
        return '%s p:%d  w:%d l:%d d%d +:%d -:%d +/-:%d pts:%d' % (self.team, self.played, self.won, self.lost, self.drawn, self.plus, self.minus, self.plus_minus, self.points)

    def __str__(self):
        return '%s p:%d  w:%d l:%d d%d +:%d -:%d +/-:%d pts:%d' % (self.team, self.played, self.won, self.lost, self.drawn, self.plus, self.minus, self.plus_minus, self.points)

    def __cmp__(self, other):
        if (self.phase.category == other.phase.category):
            if (self.phase.round == other.phase.round):
                if (self.points == other.points):
                    return self.plus_minus.__cmp__(other.plus_minus)
                else:
                    return self.points.__cmp__(other.points)
            else:
                #return re.sub("\W+", "", self.phase.round.lower()).__cmp__(re.sub("\W+", "", other.phase.round))
                #return cmp(re.sub("\W+", "", self.phase.round.lower()), re.sub("\W+", "", other.phase.round)))
                return cmp(self.phase.round, other.phase.round)
        else:
            return self.phase.category.__cmp__(other.phase.category)

    def __init__(self, team, phase):
        self.team = team
        self.phase = phase

    def __eq__(self, other):
        self.team.id == other.team.id

    def add_game(self, game):
        if (game.local.id == self.team.id):
            if (game.local_score > game.visitor_score):
                self.won += 1
                self.points += WIN_POINTS()
            elif (game.local_score < game.visitor_score):
                self.lost += 1
                self.points += LOST_POINTS()
            elif (game.local_score == game.visitor_score):
                self.drawn += 1
                self.points += DRAW_POINTS()
            else:
                raise Exception('Wrong score for game %s' % (game))
            self.plus += game.local_score
            self.minus += game.visitor_score
            self.plus_minus += game.local_score - game.visitor_score
        elif(game.visitor.id == self.team.id):
            if (game.local_score < game.visitor_score):
                self.won += 1
                self.points += WIN_POINTS()
            elif (game.local_score > game.visitor_score):
                self.lost += 1
                self.points += LOST_POINTS()
            elif (game.local_score == game.visitor_score):
                self.drawn += 1
                self.points += DRAW_POINTS()           
            else:
                raise Exception('Wrong score for game %s' % (game))
            self.plus += game.visitor_score
            self.minus += game.local_score
            self.plus_minus += game.visitor_score - game.local_score
        else:
            raise Exception('Expected team %s in the game but not found.' % (self.team))
        self.played += 1
                
    
class Fixtures:
    liga_games = {}
    pool_games = {}
    playoff_games = {}
    pool_rows = {}
    liga_clasification = []
    sorted_pools_rows = []
    sorted_pools = {}

    def __init__(self, games):
        self.liga_clasification = []
        self.pool_rows = {}

        for game in games:
            if game.phase.round == GameRound.LIGA:
                self.liga_games.update({game.id:game})
            elif (game.phase.round == GameRound.POOL_A 
                  or game.phase.round == GameRound.POOL_B        
                  or game.phase.round == GameRound.POOL_C
                  or game.phase.round == GameRound.POOL_D):
                self.pool_games.update({game.id:game})
            else:
                self.playoff_games.update({game.id:game})
                
        for game in self.pool_games.values():
            if (self.pool_rows.has_key(game.local.id)):
                row = self.pool_rows.get(game.local.id)
                row.add_game(game)                
            else:
                row = ClassificationRow(game.local, game.phase)
                row.add_game(game)

            self.pool_rows.update({game.local.id:row})

            if (self.pool_rows.has_key(game.visitor.id)):
                row = self.pool_rows.get(game.visitor.id)
                row.add_game(game)
            else:
                row = ClassificationRow(game.visitor, game.phase)
                row.add_game(game)

            self.pool_rows.update({game.visitor.id:row})

    def sort_pools_rows(self):        
#        self.sorted_pools = sorted(self.pool_rows.values(), key=attrgetter('points'))
        self.sorted_pools_rows = sorted(self.pool_rows.values(), reverse=True)

    def sort_pools(self):
        self.sorted_pools_rows = sorted(self.pool_rows.values(), reverse=True)
        self.sorted_pools.clear()
        row_list = []
        old_pool = self.sorted_pools_rows[0].phase.round
        for item in self.sorted_pools_rows:
            new_pool = item.phase.round
            if (old_pool != new_pool):
                row_list= []
            row_list.append(item)
            self.sorted_pools.update({item.phase.round:row_list})
            old_pool = new_pool
            
    def get_games(self, games, arg, result):
        result = []
        for game in games:
            if game.phase.round == arg:
                result.append(game)
        return result
        
    
def WIN_POINTS():
    return 4

def DRAW_POINTS():
    return 2

def LOST_POINTS():
    return 1

    
        
