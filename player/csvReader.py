import csv
import logging

import itertools

from player import csvdata
from player.models import Game
from player.models import GameField
from player.models import GameRound
from player.models import Person
from player.models import Player
from player.models import PlayerStadistic
from player.models import Team
from player.models import Tournament

from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

# Get an instance of a logger
logger = logging.getLogger(__name__)


class DjangoSimpleFetcher:
    @staticmethod
    def print_fetch_result(obj, created=False):
        if created:
            print('Created {:s}:\n'.format(type(obj).__name__) + str(obj))
            logger.debug('Created {:s}:\n'.format(type(obj).__name__) + str(obj))

        else:
            if obj is None:
                print('Neither object found or created.\n')
                logger.debug('Neither object found or created.\n')
            else:
                print('Found {:s}:\n'.format(type(obj).__name__) + str(obj))
                logger.debug('Found {:s}:\n'.format(type(obj).__name__) + str(obj))

    @staticmethod
    def get_or_create_tournament(tournament_name, tournament_division):
        result = Tournament.objects.get_or_create(name=tournament_name, division=tournament_division)
        return result

    @staticmethod
    def get_team(team_name, division):
        return Team.objects.get(name=team_name, division=division)

    @staticmethod
    def get_or_create_team(team_name, team_division):
        result = Team.objects.get_or_create(name=team_name, division=team_division)
        return result

    @staticmethod
    def get_or_create_person(first_name, last_name, gender=None):
        try:
            result = Person.objects.get(first_name=first_name, last_name=last_name)
            result = result, False
        except MultipleObjectsReturned:
            if gender:
                result = Person.objects.get(first_name=first_name, last_name=last_name, gender=gender)
                result = result, False
        except ObjectDoesNotExist:
            if gender:
                result = Person.objects.get_or_create(first_name=first_name, last_name=last_name, gender=gender)
            else:
                result = Person.objects.get_or_create(first_name=first_name, last_name=last_name)
        return result

    @staticmethod
    def get_or_create_player(person, team, number, tournament_id=None):
        try:
            number2 = int(number)
        except ValueError:
            number2 = None
        obj, created = Player.objects.get_or_create(person=person, team=team, number=number2)
        if tournament_id is None:
            pass
        else:
            obj.tournaments_played.add(tournament_id)
        return obj, created

    @staticmethod
    def get_game(tournament, phase, local, local_score, visitor, visitor_score, strict=True):
        try:
            # first try with given local and visitor teams and scores:
            game = Game.objects.get(
                    tournament=tournament,
                    local=local,
                    visitor=visitor,
                    local_score=local_score,
                    visitor_score=visitor_score,
                    phase=phase)
            return game
        except Game.DoesNotExist as ex:
            if strict:
                raise ex
        # else: ignore exception and go for a second try changing local and visitor teams and scores:
        game = Game.objects.get(
                tournament=tournament,
                visitor=local,
                local=visitor,
                visitor_score=local_score,
                local_score=visitor_score,
                phase=phase)
        return game

    @staticmethod
    def create_game(tournament, phase, field, time, local_team, visitor_team, local_score, visitor_score):
        result = Game.objects.get_or_create(
                tournament=tournament,
                local=local_team,
                visitor=visitor_team,
                local_score=local_score,
                visitor_score=visitor_score,
                phase=phase,
                field=field,
                time=time)
        return result

    @staticmethod
    def get_or_create_game_phase(category, round, number, create):
        get_round = round
        print(get_round.encode('utf-8'))
        if get_round.encode('utf-8') == b'\xc2\xbc' or get_round.encode(
                'utf-8') == b'\xc2\xbd' or get_round == '\xc2\xbc':
            get_round = '1/4'
        if create:
            result = GameRound.objects.get_or_create(category=category, round=get_round, number_teams=number)
        else:
            result = GameRound.objects.get(category=category, round=get_round, number_teams=number), False
        return result

    @staticmethod
    def get_or_create_nts_statistic(game, player, scores):
        if scores and int(scores) > 0:
            result = PlayerStadistic.objects.get_or_create(game=game, player=player, points=scores)
            return result
        else:
            return None, False

    @staticmethod
    def get_or_create_fit_statistic(tournament, player, played, scores, mvp):
        result = PlayerStadistic.objects.get_or_create(tournament=tournament, player=player, played=played, mvp=mvp)
        return result


class DjangoCsvFetcher:
    @staticmethod
    def create_csv_phase(csv_game, create):
        if not isinstance(csv_game, csvdata.CsvGame):
            assert 0, "Wrong game to read: " + csv_game

        round = csv_game.round
        if round.encode('utf-8') == b'\xc2\xbc':
            round = '1/4'
        print(round.encode('utf-8'))

        if create:
            result, created = GameRound.objects.get_or_create(
                    category=csv_game.category,
                    round=round,
                    number_teams=csv_game.nteams)
        else:
            result, created = GameRound.objects.get(
                    category=csv_game.category,
                    round=round,
                    number_teams=csv_game.nteams), False

        DjangoSimpleFetcher.print_fetch_result(result, created)
        return result, created

    @staticmethod
    def create_csv_game(csv_game):
        if not isinstance(csv_game, csvdata.CsvGame):
            assert 0, "Wrong game to read: " + csv_game

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(csv_game.tournament_name, csv_game.division)
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        local_team, created = create_or_fetch_team(csv_game.local, csv_game.division)
        DjangoSimpleFetcher.print_fetch_result(local_team, created)

        add_team_to_tournament(tournament, local_team)
        # if created:
        #    add_team_to_tournament(tournament, local_team)
        phase, created = DjangoCsvFetcher.create_csv_phase(csv_game, False)
        time = csv_game.time if csv_game.time else None

        if csv_game.field:
            field, created = GameField.objects.get_or_create(name=csv_game.field)
            DjangoSimpleFetcher.print_fetch_result(field, created)
        else:
            field = None

        visitor_team, created = create_or_fetch_team(csv_game.visitor, csv_game.division)
        DjangoSimpleFetcher.print_fetch_result(visitor_team, created)

        add_team_to_tournament(tournament, visitor_team)
        # if created:
        #    add_team_to_tournament(tournament, visitor_team)

        game, created = DjangoSimpleFetcher.create_game(
                tournament, phase, field, time, local_team, visitor_team, csv_game.local_score, csv_game.visitor_score)
        DjangoSimpleFetcher.print_fetch_result(game, created)
        # assert created, "The game already exists"

    @staticmethod
    def create_or_fetch_person(row):
        print(row)
        try:
            result = Person.objects.get(
                    first_name=row[csvdata.PL_ST_FIRST_NAME_INDEX],
                    last_name=row[csvdata.PL_ST_LAST_NAME_INDEX])
            result = result, False

        except MultipleObjectsReturned:
            if row[csvdata.PL_ST_GENDER_INDEX]:
                result = Person.objects.get(
                        first_name=row[csvdata.PL_ST_FIRST_NAME_INDEX],
                        last_name=row[csvdata.PL_ST_LAST_NAME_INDEX],
                        gender=row[csvdata.PL_ST_GENDER_INDEX])
            result = result, False

        except ObjectDoesNotExist:
            if row[csvdata.PL_ST_GENDER_INDEX]:
                result = Person.objects.get_or_create(
                        first_name=row[csvdata.PL_ST_FIRST_NAME_INDEX],
                        last_name=row[csvdata.PL_ST_LAST_NAME_INDEX],
                        gender=row[csvdata.csvdata.PL_ST_GENDER_INDEX])
            else:
                result = Person.objects.get_or_create(
                        first_name=row[csvdata.PL_ST_FIRST_NAME_INDEX],
                        last_name=row[csvdata.PL_ST_LAST_NAME_INDEX])
        return result

    @staticmethod
    def create_csv_fit_statistic(csv_stats):
        if not isinstance(csv_stats, csvdata.FitStatistic):
            assert 0, "Wrong statistic to read: " + csv_stats

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(
                csv_stats.tournament_name,
                csv_stats.division)
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        team, created = DjangoSimpleFetcher.get_or_create_team(csv_stats.team, csv_stats.division)
        DjangoSimpleFetcher.print_fetch_result(team, created)

        person, created = DjangoSimpleFetcher.get_or_create_person(
                csv_stats.first_name,
                csv_stats.last_name,
                csv_stats.gender)
        DjangoSimpleFetcher.print_fetch_result(person, created)

        player, created = DjangoSimpleFetcher.get_or_create_player(person, team, csv_stats.number, tournament)
        DjangoSimpleFetcher.print_fetch_result(player, created)

        fit_stat, created = DjangoSimpleFetcher.get_or_create_fit_statistic(tournament, player, csv_stats.played,
                                                                            csv_stats.scores, csv_stats.mvp)
        DjangoSimpleFetcher.print_fetch_result(fit_stat, created)

    @staticmethod
    def create_csv_nts_player_statistic(csv_stats):
        if not isinstance(csv_stats, csvdata.CsvNTSStatistic):
            assert 0, "Wrong stadistic to read: " + csv_stats

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(
                csv_stats.tournament_name,
                csv_stats.division)
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        team, created = DjangoSimpleFetcher.get_or_create_team(csv_stats.team, csv_stats.division)
        DjangoSimpleFetcher.print_fetch_result(team, created)

        person, created = DjangoSimpleFetcher.get_or_create_person(
                csv_stats.first_name,
                csv_stats.last_name,
                csv_stats.gender)
        DjangoSimpleFetcher.print_fetch_result(person, created)

        player, created = DjangoSimpleFetcher.get_or_create_player(person, team, csv_stats.number, tournament)
        DjangoSimpleFetcher.print_fetch_result(player, created)

        if csv_stats.visitor_score:  # if true nts stadistic otherwise player insert.
            local_team = DjangoSimpleFetcher.get_team(csv_stats.local, csv_stats.division)
            DjangoSimpleFetcher.print_fetch_result(local_team)

            visitor_team = DjangoSimpleFetcher.get_team(csv_stats.visitor, csv_stats.division)
            DjangoSimpleFetcher.print_fetch_result(visitor_team)

            phase, created = DjangoSimpleFetcher.get_or_create_game_phase(
                    csv_stats.category, csv_stats.round, csv_stats.team_numbers, False)
            DjangoSimpleFetcher.print_fetch_result(phase, created)

            game = DjangoSimpleFetcher.get_game(tournament, phase, local_team, csv_stats.local_score,
                                                visitor_team, csv_stats.visitor_score, False)
            DjangoSimpleFetcher.print_fetch_result(game)

            nts_stat, created = DjangoSimpleFetcher.get_or_create_nts_statistic(
                    game, player, csv_stats.tries)
            DjangoSimpleFetcher.print_fetch_result(nts_stat, created)
        else:
            print('GameStadistic skipped: there are no tries for player: {:s}\n '.format(str(player)))


def add_team_to_tournament(tournament, team):
    if not tournament.teams.filter(id=team.id).exists():
        tournament.teams.add(team)
        tournament.save()
        print("Added team %s into tournament %s" % (team.name, tournament.name))
    else:
        print("Tournament %s already has the team %s" % (tournament.name, team.name))


def create_or_fetch_team(pName, pDivision):
    result = Team.objects.get_or_create(
            name=pName,
            division=pDivision,
    )
    return result


def printCF(obj, created):
    if obj:
        if created:
            print('Created {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
        else:
            print('Found {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
    else:
        print('ERROR\n')


class CsvReader:
    (PHASE, TOURNAMENT, NTS_STATISTIC, FIT_STATISTIC) = (0, 1, 2, 3)

    def __init__(self, type):
        if type in [self.PHASE, self.TOURNAMENT, self.NTS_STATISTIC, self.FIT_STATISTIC]:
            self._fexit = '####'
            self._exit_text = '\n Force exit #### :)\n'
            self._type = type
        else:
            assert 0, "Wrong reader creation: " + type
            #        if type == "phase": return csvPhasesReader()
            #        if type == "tournament": return csvTournamentReader()
            #        if type == "ntsstadistic": return ntsStadisticReader()
            #        assert 0, "Wrong reader creation: "+ type
            #    factory = staticmethod(factory)

    @staticmethod
    def print_row_to_read(csv):
        print('\nRow to read:\n' + str(csv) + '\n')

    def print_file_footer(self, arg):
        print('\nFinished reading {:s}...\n'.format(arg))

    def print_fetch_result(self, obj, created):
        if created:
            print('Created {:s}:\n'.format(self._type) + str(obj))
        else:
            print('Found {:s}:\n'.format(self._type) + str(obj))

    def get_csv_object(self, row):
        if self._type == self.PHASE:
            result = csvdata.CsvPhase(row)
        elif self._type == self.TOURNAMENT:
            result = csvdata.CsvGame(row, None, None, None)
        elif self._type == self.NTS_STATISTIC:
            result = csvdata.CsvNTSStatistic(row)
        elif self._type == self.FIT_STATISTIC:
            result = csvdata.FitStatistic.from_array(row)
        else:
            assert 0, "Wrong object to read: " + self._type
        return result

    def create_django_object(self, csv_object):
        if self._type == self.PHASE and isinstance(csv_object, csvdata.CsvPhase):
            phase, created = DjangoSimpleFetcher.get_or_create_game_phase(
                    csv_object.category, csv_object.round, csv_object.teams, True)
            DjangoSimpleFetcher.print_fetch_result(phase, created)
        elif self._type == self.TOURNAMENT and isinstance(csv_object, csvdata.CsvGame):
            DjangoCsvFetcher.create_csv_game(csv_object)
        elif self._type == self.NTS_STATISTIC and isinstance(csv_object, csvdata.CsvNTSStatistic):
            DjangoCsvFetcher.create_csv_nts_player_statistic(csv_object)
        elif self._type == self.FIT_STATISTIC and isinstance(csv_object, csvdata.FitStatistic):
            DjangoCsvFetcher.create_csv_fit_statistic(csv_object)
        else:
            assert 0, "Wrong object to read: " + self._type

    def read_file(self, file, subclass):
        with open(file, 'rt', encoding='utf-8') as csv_file:
            # reader2 = csv.reader(csv_file, delimiter=';')
            reader1, reader2 = itertools.tee(csv.reader(csv_file, delimiter=';'))
            columns = len(next(reader1))
            del reader1
            print('\nDetected %s columns\n' % columns)
            print('\nStarting reading {:n} from {:s}\n'.format(self._type, file))
            for row in reader2:
                if any(row):
                    if row[0] == self._fexit:
                        print(self._exit_text)
                        break
                    self.print_row_to_read(row)
                    csv_object = self.get_csv_object(row)
                    self.create_django_object(csv_object)
        csv_file.close()
        print('\nFinished reading {:s}...[0=PHASE, 1=TOURNAMENT, 2=NTS_STADISTIC]\n'.format(str(self._type)))
