from player.models import GameRound
from operator import attrgetter
import re
import collections

class StructuresUtils:
    def get_team_view_games(self, games):
        result = {}
        for game in games:
            if (result.has_key(game.phase)):
                phase_games = result.get(game.phase)
            else:
                phase_games = []
            phase_games.append(game)
            result.update({game.phase:phase_games})
        return result

    def get_teams_matrix(self, teams, columns_number):
        if not (columns_number > 0):
            raise ValueError('Argument columns_number must be a positive integer. Received : %s' % (columns_number))
        column_size = len(teams) / columns_number
        if (len(teams) % column_size > 0):
            column_size += 1

#        matrix = [[0 for x in xrange(column_size)] for x in xrange(columns_number)]
        matrix = []
        for x in range(column_size):
            matrix.append([])
        i = 0
        for team in teams:
            matrix[i % column_size].append(team)
            i += 1
        return matrix

    def get_game_details_matrix(self, stadistics, local_players, visitor_players):
        result = []
        n_rows = len(local_players) if len(local_players) > len(visitor_players) else len(visitor_players)
        for i in range(n_rows):
            if(i < len(local_players)):
                points = 0
                number = local_players[i].number if local_players[i].number else ''
                for st in stadistics:
                    if(st.player == local_players[i]):
                        points = st.points
                        break
                if(points > 0):
                    row = [number, local_players[i].person, points]
                else:
                    row = [number, local_players[i].person, '-']
            else:
                row = ['', '', '']                    
            if(i < len(visitor_players)):
                points = 0
                number = visitor_players[i].number if visitor_players[i].number else ''
                for st in stadistics:
                    if(st.player == visitor_players[i]):
                        points = st.points
                        break
                if(points > 0):
                    row.extend([number, visitor_players[i].person, points])
                else:
                    row.extend([number, visitor_players[i].person, '-'])
            else:
                row.extend(['', '', ''])
                
            result.append(row)
        return result         

    def get_team_details_matrix(self, stadistics, players):
        result = []
        for player in players:
            points = 0
            for st in stadistics:
                if (st.player == player):
                    points += st.points
            result.append([player.number, player.person, points])
        return result

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
                #print('cmp_round(%s, %s) return %s.' % (self.phase.round, other.phase.round, self.cmp_round(other.phase.round)))
                return cmp(self.phase.round, other.phase.round)

        else:
            return self.phase.category.__cmp__(other.phase.category)

    def __init__(self, team, phase):
        self.team = team
        self.phase = phase

    def __eq__(self, other):
        self.team.id == other.team.id

    def cmp_round(self, other):
        if (self.phase.round == other):
            return 0
        elif (self.phase.round == GameRound.POOL_A):
            return -1
        elif (other == GameRound.POOL_A):
            return 1
        elif (self.phase.round == GameRound.POOL_B):
            return -1
        elif (other == GameRound.POOL_B):
            return 1
        elif (self.phase.round == GameRound.POOL_C):
            return -1
        elif (other == GameRound.POOL_C):
            return 1
        else:
            raise Exception('Game.Round combination (%s, %s) is not allowed.' % (self.phase.round, other))


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
    sorted_pools_rows = []
    sorted_pools = {}
    games = {}

    def __init__(self, games):
        self.games = {}
        self.liga_games = {}
        self.pool_rows = {}
        self.pool_games = {}
        self.sorted_pools_rows = []
        self.sorted_pools = {}

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

            if self.games.has_key(game.phase):
                phase_games = self.games.get(game.phase)
                phase_games.update({game.id:game})
            else:
                self.games.update({game.phase:{game.id:game}})

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

    def sort_pools(self):
        self.sorted_pools_rows = sorted(self.pool_rows.values(), reverse=True)
        self.sorted_pools.clear()
        row_list = []
        #print(self.pool_rows)
        #print(self.sorted_pools_rows)
        if len(self.sorted_pools_rows) == 0:
            return []
        old_pool = self.sorted_pools_rows[0].phase.round
        for item in self.sorted_pools_rows:
            new_pool = item.phase.round
            if (old_pool != new_pool):
                row_list= []
            row_list.append(item)
            self.sorted_pools.update({item.phase.round:row_list})
            old_pool = new_pool
        self.sorted_pools = collections.OrderedDict(sorted(self.sorted_pools.items()))
        
    def get_finals(self, result):
        result = {}
        for key in self.games:
            if (key.round == GameRound.FINAL
                or key.round == GameRound.THIRD_PLACE
                or key.round == GameRound.SEMI
                or key.round == GameRound.QUARTER 
                or key.round == GameRound.EIGHTH 
                or key.round == GameRound.SIXTEENTH):
                result[key] = self.games[key]
                #result.update({key:self.games[key]})
                #return sorted(result.values(), reverse=True)
        return collections.OrderedDict(sorted(result.items()))

    def get_phased_finals(self, result):
        result = {}
        sorted_result = collections.OrderedDict()
        finals = self.get_finals({})
        oldphase = GameRound.GOLD
        variable = {}
        for key in finals:
            if key.category != oldphase:
                variable = {}
                oldphase = key.category
            variable.update({key:finals[key]})
            #result.update({key.category:variable})
            result.update({key.category:collections.OrderedDict(sorted(variable.items()))})
        if result:
            if result.get(GameRound.GOLD):
                sorted_result[GameRound.GOLD] = result[GameRound.GOLD]
            if result.get(GameRound.SILVER):
                sorted_result[GameRound.SILVER] = result[GameRound.SILVER]
            if result.get(GameRound.BRONZE):
                sorted_result[GameRound.BRONZE] = result[GameRound.BRONZE]
            if result.get(GameRound.WOOD):
                sorted_result[GameRound.WOOD] = result[GameRound.WOOD]
#        return collections.OrderedDict(sorted(result))
        return sorted_result

class TeamsMatrix:
    matrix = []
    def __init__(self, columns_number, teams):
        if not (columns_number > 0):
            raise ValueError('Argument columns_number must be a positive integer. Received : %s' % (columns_number))
        #self.teams_matrix[columns_numbers][]
        self.matrix = []
        column_size = len(teams) / columns_number
        column = []
        i = 0
        for team in teams:
            column.append(team)
            if (i == column_size-1):
                i = 0
                self.matrix.append(column)
                column = []
            else:
                i += 1

    
def WIN_POINTS():
    return 4

def DRAW_POINTS():
    return 2

def LOST_POINTS():
    return 1
