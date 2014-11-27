from django.views.generic import DetailView
from player.models import Game, Player, PlayerStadistic, Tournament, Team
from django.db.models import Q
from service import *

class GameView(DetailView):

    model = Game
    template_name = 'tournaments/detail_game.html'

    def get_context_data(self, **kwargs):
        local_players = Player.objects.filter(team=self.object.local)
        visitor_players = Player.objects.filter(team=self.object.visitor)
        stadistics = PlayerStadistic.objects.filter(game=self.object.id)

        context = super(GameView, self).get_context_data(**kwargs)
        context['tournament_list'] = Tournament.objects.all()
        context['game'] = self.object
        context['stadistics'] = self.get_game_details_matrix(stadistics, local_players, visitor_players)

        return context
     
    # Create a matrix for being displayed by template. Each row of the matrix contains the number, person and the
    # scored tries for a local and visitor players. If any local or visitor team has more players than the other 
    # team the remaining cells will be empty.
    #
    # @param stadistics       The stadistics for the game
    # @param local_players    The local team players of the game
    # @param visitor_players  The visitor team players of the game
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

class TeamView(DetailView):
    
    model = Team;
    template_name = 'tournaments/detail_team.html'

    def get_context_data(self, **kwargs):
        tournament_id = self.kwargs.get('tournament_id')
        players = Player.objects.filter(team=self.object.id, tournaments_played__id=tournament_id).distinct()
        games = Game.objects.filter(Q(tournament=tournament_id), 
                                    Q(local=self.object.id) | Q(visitor=self.object.id))

        context = super(TeamView, self).get_context_data(**kwargs)
        context['team'] = self.object
        context['tournament_list'] = Tournament.objects.all()
        context['games'] = self.sort_games_by_phases(games)
        context['players'] = self.get_player_stadistics(players, games)
        
        return context

    # Sort a list of games by phases. The result is a dictionary where each element is a list of games of the same
    # phase of a tournament.
    #
    # @param games The list of games to be sorted.
    def sort_games_by_phases(self, games):
        result = {}
        for game in games:
            if (result.has_key(game.phase)):
                phase_games = result.get(game.phase)
            else:
                phase_games = []
            phase_games.append(game)
            result.update({game.phase:phase_games})
        return result

    # Given a list of players a list with players and the total amount of points in a tournament is returned.
    #
    # @param players The list of players to find out the scored points.
    def get_player_stadistics(self, players, games):
        result = []
        stadistics = []

        for player in players:
            stadistics.extend(PlayerStadistic.objects.filter(Q(player=player.id), Q(game__in=games)))

        for player in players:
            points = 0
            for st in stadistics:
                if (st.player == player):
                    points += st.points
            result.append([player.number, player.person, points])

        return result

class TournamentView(DetailView):
    model = Tournament
    template_name = 'tournaments/detail_tournament2.html'

    def get_context_data(self, **kwargs):
        games = Game.objects.filter(tournament=self.object.id)
        teams = Team.objects.filter(tournament__id=self.object.id)
        
        fixtures = Fixtures(games)
        fixtures.sort_pools()
        pool_games = fixtures.sorted_pools
        finals_games = fixtures.get_phased_finals({})
        st_utils = StructuresUtils()

        context = super(TournamentView, self).get_context_data(**kwargs)        
        context['tournament'] = self.object
        context['tournament_list'] = Tournament.objects.all()
        context['games'] = games
        context['liga_games'] = fixtures.liga_games
        context['pool_games'] = pool_games
        context['finals_games'] = finals_games
        context['phased_finals_games'] = fixtures.get_phased_finals({})
        context['teams_matrix'] = st_utils.get_teams_matrix(teams, 4)

        return context

