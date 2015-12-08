from django.views.generic import DetailView
from django.db.models import Q

from player.models import Game
from player.models import GameRound
from player.models import Player
from player.models import PlayerStadistic
from player.models import Tournament
from player.models import Team
from player.models import Person

from player.service import Fixtures
from player.service import StructuresUtils

class GameView(DetailView):

    model = Game
    template_name = 'tournaments/detail_game.html'

    def get_context_data(self, **kwargs):
        local_players = Player.objects.filter(team = self.object.local, tournaments_played = self.object.tournament)
        visitor_players = Player.objects.filter(team = self.object.visitor, tournaments_played = self.object.tournament)
        stadistics = PlayerStadistic.objects.filter(game = self.object.id)

        context = super(GameView, self).get_context_data(**kwargs)
        context['tournament_list'] = Tournament.objects.all()
        context['game'] = self.object
        context['stadistics'] = self.get_game_details_matrix(stadistics,
                                                             local_players,
                                                             visitor_players)
        return context
     
    def get_game_details_matrix(self, stadistics, local_players, visitor_players):
        """
        Create a matrix with the content of the stadistics for all the players of a game. Only the
        detail_gamem template is designed to display this matrix data.

        Args:
            stadistics:      The stadistics for the game
            local_players:   The local team players of the game
            visitor_players: The visitor team players of the game

        Returns:
            A matrix with sorted stadistics of a game. Each row of the matrix contains the number,
            person and the scored tries for a local and visitor players. If any local  or visitor
            team has more players than the other team the remaining cells will be empty.
        """

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

class PersonView(DetailView):
    model = Person
    template_name = 'tournaments/detail_person.html'

    def get_context_data(self, **kwargs):
        games = Game.objects.filter(Q(local=self.object.id) | Q(visitor=self.object.id))
        played_tournaments = Tournament.objects.filter(teams__id=self.object.id)

        context = super(PersonView, self).get_context_data(**kwargs)
        context['person'] = self.object
        context['tournament_list'] = Tournament.objects.all()
        context['played_tournaments'] = played_tournaments

        return context

class TeamView(DetailView):
    model = Team
    template_name = 'tournaments/detail_team.html'

    def get_context_data(self, **kwargs):
        games = Game.objects.filter(Q(local=self.object.id) | Q(visitor=self.object.id))
        played_tournaments = Tournament.objects.filter(teams__id=self.object.id)

        context = super(TeamView, self).get_context_data(**kwargs)
        context['team'] = self.object
        context['tournament_list'] = Tournament.objects.all()
        context['played_tournaments'] = played_tournaments
        context['games'] = games

        return context

class TeamTournamentView(DetailView):
    
    model = Team;
    template_name = 'tournaments/detail_team_tournament.html'

    def get_context_data(self, **kwargs):
        tournament_id = self.kwargs.get('tournament_id')
        players = Player.objects.filter(team=self.object.id,
                                        tournaments_played__id=tournament_id).distinct()
        games = Game.objects.filter(Q(tournament=tournament_id), 
                                    Q(local=self.object.id) | Q(visitor=self.object.id))

        context = super(TeamTournamentView, self).get_context_data(**kwargs)
        context['team'] = self.object
        context['tournament_list'] = Tournament.objects.all()
        context['games'] = self.sort_games_by_phases(games)
        context['players'] = self.get_player_stadistics(players, games)
        
        return context

    def sort_games_by_phases(self, games):
        """
        Sort a list of games by phases.

        Args:
            games: A collection of games.

        Returns:
            The result is an ordered dictionary where each element is a list of games of the same 
            phase of a tournament. The dictionary is an ordered by the key.round which is an phase object.
        """

        d_all = {}
        for game in games:
            if (d_all.has_key(game.phase)):
                phase_games = d_all.get(game.phase)
            else:
                phase_games = []
            phase_games.append(game)
            d_all.update({game.phase:phase_games})

        d_pools = {}
        d_finals = {}
        l_finals = []
        for k,v in d_all.iteritems():
            if (GameRound.is_pool(k)):
                d_pools.update({k:v})
            else:
                d_finals.update({k:v})
                l_finals.append(k)

        result = collections.OrderedDict()
        for k in (sorted(d_pools)):
            result.update({k:d_pools.get(k)})
        for k in (sorted(l_finals, key=lambda final: GameRound.ordered_rounds.index(final.round), reverse=True)):
            result.update({k:d_finals.get(k)})

        return result

    def get_player_stadistics(self, players, games):
        """
        Given a list of players, a list with the same players and their total amount of points in a
        tournament is returned.

        Args:
            players: The list of players to find out the scored points.

        Returns:
            The result is a dictionary where each element is a list of games of the same phase
            of a tournament.
        """

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

        return sorted(result, key=lambda line: line[0])

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
