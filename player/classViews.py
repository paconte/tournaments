from django.views.generic import DetailView
from django.db.models import Q

from collections import OrderedDict

from player.models import Game
from player.models import GameRound
from player.models import Player
from player.models import PlayerStadistic
from player.models import Tournament
from player.models import Team
from player.models import Person
from player.service import Fixtures
from player.service import StructuresUtils
from player.games import PadelResult

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GameView(DetailView):
    model = Game
    template_name = 'detail_game.html'

    def get_context_data(self, **kwargs):
        local_players = Player.objects.filter(team=self.object.local, tournaments_played=self.object.tournament)
        visitor_players = Player.objects.filter(team=self.object.visitor, tournaments_played=self.object.tournament)
        statistics = PlayerStadistic.objects.filter(game=self.object.id)
        local_stats, visitor_stats = self.get_game_details_stats(statistics, local_players, visitor_players)

        context = super(GameView, self).get_context_data(**kwargs)
        context['game'] = self.object
        context['statistics'] = True if len(statistics) > 0 else False
        context['local_stats'] = local_stats
        context['visitor_stats'] = visitor_stats

        return context

    def get_game_details_stats(self, statistics, local_players, visitor_players):
        """
        Create a matrix with the content of the stadistics for all the players of a game. Only the
        detail_gamem template is designed to display this matrix data.

        Args:
            statistics:      The stadistics for the game
            local_players:   The local team players of the game
            visitor_players: The visitor team players of the game

        Returns:
            A matrix with sorted stadistics of a game. Each row of the matrix contains the number,
            person and the scored tries for a local and visitor players. If any local  or visitor
            team has more players than the other team the remaining cells will be empty.
        """
        local_stats = dict()
        visitor_stats = dict()
        n_rows = len(local_players)
        for i in range(n_rows):
            points = 0
            number = local_players[i].number if local_players[i].number else ''
            for st in statistics:
                if st.player == local_players[i]:
                    points = st.points
                    break
            # row = [number, local_players[i].person, points]
            if local_players[i].person in local_stats.keys():
                local_stats[local_players[i].person] = local_stats[local_players[i].person] + points
            else:
                local_stats[local_players[i].person] = points

        n_rows = len(visitor_players)
        for i in range(n_rows):
            points = 0
            number = visitor_players[i].number if visitor_players[i].number else ''
            for st in statistics:
                if st.player == visitor_players[i]:
                    points = st.points
                    break
            # row = [number, visitor_players[i].person, points]
            # visitor_stats.append(row)
            if visitor_players[i].person in visitor_stats.keys():
                visitor_stats[visitor_players[i].person] = visitor_stats[visitor_players[i].person] + points
            else:
                visitor_stats[visitor_players[i].person] = points

        local_stats2 = []
        for person, v in local_stats.items():
            local_stats2.append([person.get_full_name(), v, person.id])

        visitor_stats2 = []
        for person, v in visitor_stats.items():
            visitor_stats2.append([person.get_full_name(), v, person.id])

        return sorted(local_stats2, key=lambda line: line[1], reverse=True), sorted(visitor_stats2,
                                                                                    key=lambda line: line[1],
                                                                                    reverse=True)


class PersonView(DetailView):
    model = Person
    template_name = 'detail_person.html'

    def get_context_data(self, **kwargs):
        players = Player.objects.filter(person=self.object.id)
        tournament_team_dict = {}
        for player in players:
            team = player.team
            for tournament in player.tournaments_played.all():
                try:
                    teams = tournament_team_dict[tournament]
                except KeyError:
                    tournament_team_dict[tournament] = list()
                    teams = tournament_team_dict[tournament]
                teams.append(team)
                tournament_team_dict[tournament] = teams
        games = []
        for tournie, teams in tournament_team_dict.items():
            for team in teams:
                games.extend(Game.objects.filter(Q(tournament=tournie), Q(local=team) | Q(visitor=team)))
        games = sorted(games, key=lambda game: game.tournament)

        context = super(PersonView, self).get_context_data(**kwargs)
        context['person'] = self.object
        context['games'] = games
        context['tournament_team_dict'] = OrderedDict(sorted(tournament_team_dict.items()))

        return context


class TeamView(DetailView):
    model = Team
    template_name = 'detail_team.html'

    def get_context_data(self, **kwargs):
        games = Game.objects.filter(Q(local=self.object.id) | Q(visitor=self.object.id)).order_by('tournament')
        played_tournaments = Tournament.objects.filter(teams__id=self.object.id).order_by('-date', '-name')
        players = Player.objects.filter(team=self.object)

        persons = set()
        for player in players:
            persons.add(player.person)
        persons = sorted(list(persons))

        context = super(TeamView, self).get_context_data(**kwargs)
        context['team'] = self.object
        context['played_tournaments'] = played_tournaments
        context['games'] = games
        context['persons'] = persons

        return context


class TeamTournamentView(DetailView):
    model = Team
    template_name = 'detail_team_tournament.html'

    def get_context_data(self, **kwargs):
        tournament_id = self.kwargs.get('tournament_id')
        tournament = Tournament.objects.get(id=tournament_id)

        players = Player.objects.filter(team=self.object.id,
                                        tournaments_played__id=tournament_id).distinct()
        games = Game.objects.filter(Q(tournament=tournament_id),
                                    Q(local=self.object.id) | Q(visitor=self.object.id))

        context = super(TeamTournamentView, self).get_context_data(**kwargs)
        context['tournament'] = tournament
        context['team'] = self.object
        context['games'] = self.sort_games_by_phases(games)
        context['players'] = self.get_player_statistics(players, games, tournament_id)
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
            if game.phase in d_all:
                phase_games = d_all.get(game.phase)
            else:
                phase_games = []
            phase_games.append(game)
            d_all.update({game.phase: phase_games})

        d_liga = {}
        d_pools = {}
        d_divisions = {}
        d_finals = {}
        l_finals = []
        for k, v in d_all.items():
            if GameRound.is_pool(k):
                d_pools.update({k: v})
            elif k.round == GameRound.DIVISION:
                d_divisions.update({k: v})
            elif k.round == GameRound.LIGA:
                d_liga.update({k: v})
            else:
                d_finals.update({k: v})
                l_finals.append(k)

        result = OrderedDict()
        for k in (sorted(d_liga)):
            result.update({k: d_liga.get(k)})
        for k in (sorted(d_pools)):
            result.update({k: d_pools.get(k)})
        for k in (sorted(d_divisions)):
            result.update({k: d_divisions.get(k)})
        for k in (sorted(l_finals, key=lambda final: GameRound.ordered_rounds.index(final.round), reverse=True)):
            result.update({k: d_finals.get(k)})

        return result

    def get_player_statistics(self, players, games, tournament):
        stats_fit = self._get_player_stats_fit(players, tournament)
        if len(stats_fit) != 0:
            result = stats_fit
        else:
            result = self._get_player_stats_nts(players, games)
        return result

    def _get_player_stats_nts(self, players, games):
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
        statistics = []
        stats = dict()

        for player in players:
            statistics.extend(PlayerStadistic.objects.filter(Q(player=player.id), Q(game__in=games)))

        for player in players:
            points = 0
            for st in statistics:
                if st.player == player:
                    points += st.points
            if player.person in stats.keys():
                stats[player.person] = stats[player.person] + points
            else:
                stats[player.person] = points

        for person, v in stats.items():
            result.append([person.get_full_name(), v, person.id])

        return sorted(result, key=lambda line: line[1], reverse=True)

    def _get_player_stats_fit(self, players, tournament_id):
        statistics = []
        result = []
        for player in players:
            statistics.extend(PlayerStadistic.objects.filter(Q(player=player.id), Q(tournament=tournament_id)))
        for stat in statistics:
            fullname = stat.player.person.get_full_name()
            scores = stat.points
            player_id = stat.player.person.id
            result.append([fullname, scores, player_id])
        return sorted(result, key=lambda line: line[1], reverse=True)


class TournamentView(DetailView):
    model = Tournament
    template_name = 'detail_tournament2.html'

    def get_context_data(self, **kwargs):
        exclude_teams = ['1st Pool A', '2nd Pool A', '3rd Pool A', '4th Pool A',
                         '1st Pool B', '2nd Pool B', '3rd Pool B', '4th Pool B',
                         '1st Pool C', '2nd Pool C', '3rd Pool C', '4th Pool C',
                         '1st Pool D', '2nd Pool D', '3rd Pool D', '4th Pool D',
                         'Loser QF1', 'Loser QF2', 'Loser QF3', 'Loser QF4',
                         'Loser QF5', 'Loser QF6', 'Loser QF7', 'Loser QF8',
                         'Winner QF1', 'Winner QF2', 'Winner QF3', 'Winner QF4',
                         'Winner QF5', 'Winner QF6','Winner QF7', 'Winner QF8',
                         'Loser SF1', 'Loser SF2', 'Loser SF3', 'Loser SF4',
                         'Loser SF5', 'Loser SF6', 'Loser SF7', 'Loser SF8',
                         'Winner SF1', 'Winner SF2', 'Winner SF3', 'Winner SF4',
                         'Winner SF5', 'Winner SF6', 'Winner SF7', 'Winner SF8']

        games = Game.objects.filter(tournament=self.object.id)
        teams = Team.objects.filter(tournament__id=self.object.id).exclude(name__in=exclude_teams)

        fixtures = Fixtures(games)
        pool_games = fixtures.sorted_pools
        division_games = fixtures.sorted_divisions
        finals_games = fixtures.get_phased_finals({})
        st_utils = StructuresUtils()

        context = super(TournamentView, self).get_context_data(**kwargs)
        context['tournament'] = self.object
        context['games'] = games
        context['liga_games'] = fixtures.sorted_ligas
        context['pool_games'] = pool_games
        context['division_games'] = division_games
        context['finals_games'] = finals_games
        context['phased_finals_games'] = fixtures.get_phased_finals({})
        context['teams_matrix'] = st_utils.get_teams_matrix(teams, 4)

        return context
