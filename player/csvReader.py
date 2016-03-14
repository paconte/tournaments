import csv
import os.path
import logging

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

# PHASES_INDEXES
PH_PHASE_ROUND_INDEX = 0
PH_CATEGORY_INDEX = 1
PH_PHASE_TEAMS_INDEX = 2
# PLAYER_STADISTICS_INDEXES
PL_ST_TOURNAMENT_INDEX = 0
PL_ST_DIVISION_INDEX = 1
PL_ST_TEAM_INDEX = 2
PL_ST_NUMBER_INDEX = 3
PL_ST_FIRST_NAME_INDEX = 4
PL_ST_LAST_NAME_INDEX = 5
PL_ST_GENDER_INDEX = 6
PL_ST_PLAYER_TRIES_INDEX = 7
PL_ST_LOCAL_TEAM_INDEX = 8
PL_ST_LOCAL_TEAM_SCORE_INDEX = 9
PL_ST_VISITOR_TEAM_SCORE_INDEX = 10
PL_ST_VISITOR_TEAM_INDEX = 11
PL_ST_GAME_CATEGORY_INDEX = 12
PL_ST_GAME_ROUND_INDEX = 13
PL_ST_PHASE_TEAMS_INDEX = 14

# TOURNAMENT_GAMES_INDEXES
TG_TOURNAMENT_INDEX = 0
TG_DIVISION_INDEX = 1
TG_DATE_INDEX = 2
TG_TIME_INDEX = 3
TG_FIELD_INDEX = 4
TG_PHASE_INDEX = 5
TG_CATEGORY_INDEX = 6
TG_PHASE_TEAMS_INDEX = 7
# TG_GAME_ROUND_INDEX = 8
TG_LOCAL_TEAM_INDEX = 9
TG_LOCAL_TEAM_SCORE_INDEX = 10
TG_VISITOR_TEAM_SCORE_INDEX = 11
TG_VISITOR_TEAM_INDEX = 12

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
    def get_or_create_player(person, team, number):
        result = Player.objects.get_or_create(
                person=person,
                team=team,
                number=number)
        return result

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
        if get_round == '\xc2\xbc':
            get_round = '1/4'
        if create:
            result = GameRound.objects.get_or_create(category=category, round=get_round, number_teams=number)
        else:
            result = GameRound.objects.get(category=category, round=get_round, number_teams=number), False
        return result

    @staticmethod
    def get_or_create_nts_stadistic(game, player, points):
        if points and int(points) > 0:
            result = PlayerStadistic.objects.get_or_create(game=game, player=player, points=points)
            return result
        else:
            return None, False


class DjangoCsvFetcher:
    @staticmethod
    def create_csv_phase(csv_game, create):
        if not isinstance(csv_game, csvdata.CsvGame):
            assert 0, "Wrong game to read: " + csv_game
        print(csv_game.round, csv_game.category, csv_game.nteams)
        if create:
            result, created = GameRound.objects.get_or_create(
                    category=csv_game.category,
                    round=csv_game.round,
                    number_teams=csv_game.nteams)
        else:
            result, created = GameRound.objects.get(
                    category=csv_game.category,
                    round=csv_game.round,
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

        if created:
            add_team_to_tournament(tournament, local_team)

        phase, created = DjangoCsvFetcher.create_csv_phase(csv_game, False)
        time = csv_game.time if csv_game.time else None

        if csv_game.field:
            field, created = GameField.objects.get_or_create(name=csv_game.field)
            DjangoSimpleFetcher.print_fetch_result(field, created)
        else:
            field = None

        visitor_team, created = create_or_fetch_team(csv_game.visitor, csv_game.division)
        DjangoSimpleFetcher.print_fetch_result(visitor_team, created)

        if created:
            add_team_to_tournament(tournament, visitor_team)

        game, created = DjangoSimpleFetcher.create_game(
                tournament, phase, field, time, local_team, visitor_team, csv_game.local_score, csv_game.visitor_score)
        DjangoSimpleFetcher.print_fetch_result(game, created)
        # assert created, "The game already exists"

    @staticmethod
    def create_or_fetch_person(row):
        print(row)
        try:
            result = Person.objects.get(
                    first_name=row[PL_ST_FIRST_NAME_INDEX],
                    last_name=row[PL_ST_LAST_NAME_INDEX])
            result = result, False

        except MultipleObjectsReturned:
            if row[PL_ST_GENDER_INDEX]:
                result = Person.objects.get(
                        first_name=row[PL_ST_FIRST_NAME_INDEX],
                        last_name=row[PL_ST_LAST_NAME_INDEX],
                        gender=row[PL_ST_GENDER_INDEX])
            result = result, False

        except ObjectDoesNotExist:
            if row[PL_ST_GENDER_INDEX]:
                result = Person.objects.get_or_create(
                        first_name=row[PL_ST_FIRST_NAME_INDEX],
                        last_name=row[PL_ST_LAST_NAME_INDEX],
                        gender=row[PL_ST_GENDER_INDEX])
            else:
                result = Person.objects.get_or_create(
                        first_name=row[PL_ST_FIRST_NAME_INDEX],
                        last_name=row[PL_ST_LAST_NAME_INDEX])
        return result

    @staticmethod
    def create_csv_nts_player_stadistic(csv_nts_stadistic):
        if not isinstance(csv_nts_stadistic, csvdata.CsvNTSStadistic):
            assert 0, "Wrong stadistic to read: " + csv_nts_stadistic

        tournament, created = DjangoSimpleFetcher.get_or_create_tournament(
                csv_nts_stadistic.tournament_name,
                csv_nts_stadistic.division)
        DjangoSimpleFetcher.print_fetch_result(tournament, created)

        team, created = DjangoSimpleFetcher.get_or_create_team(csv_nts_stadistic.team, csv_nts_stadistic.division)
        DjangoSimpleFetcher.print_fetch_result(team, created)

        person, created = DjangoSimpleFetcher.get_or_create_person(
                csv_nts_stadistic.first_name,
                csv_nts_stadistic.last_name,
                csv_nts_stadistic.gender)
        DjangoSimpleFetcher.print_fetch_result(person, created)

        player, created = DjangoSimpleFetcher.get_or_create_player(person, team, csv_nts_stadistic.number)
        DjangoSimpleFetcher.print_fetch_result(player, created)

        if csv_nts_stadistic.visitor_score:  # if true nts stadistic otherwise player insert.
            local_team = DjangoSimpleFetcher.get_team(csv_nts_stadistic.local, csv_nts_stadistic.division)
            DjangoSimpleFetcher.print_fetch_result(local_team)

            visitor_team = DjangoSimpleFetcher.get_team(csv_nts_stadistic.visitor, csv_nts_stadistic.division)
            DjangoSimpleFetcher.print_fetch_result(visitor_team)

            phase, created = DjangoSimpleFetcher.get_or_create_game_phase(
                    csv_nts_stadistic.category, csv_nts_stadistic.round, csv_nts_stadistic.team_numbers, False)
            DjangoSimpleFetcher.print_fetch_result(phase, created)

            game = DjangoSimpleFetcher.get_game(tournament, phase, local_team, csv_nts_stadistic.local_score,
                                                visitor_team, csv_nts_stadistic.visitor_score, False)
            DjangoSimpleFetcher.print_fetch_result(game)

            nts_stadistic, created = DjangoSimpleFetcher.get_or_create_nts_stadistic(
                    game, player, csv_nts_stadistic.tries)
            DjangoSimpleFetcher.print_fetch_result(nts_stadistic, created)
        else:
            print('GameStadistic skipped: there are no tries for player: {:s}\n '.format(str(player)))


def add_team_to_tournament(tournament, team):
    tournament.teams.add(team)
    tournament.save()


def create_or_fetch_person(row):
    try:
        result = Person.objects.get(
                first_name=row[PL_ST_FIRST_NAME_INDEX],
                last_name=row[PL_ST_LAST_NAME_INDEX]
        )
        result = result, False
    except MultipleObjectsReturned:
        if row[PL_ST_GENDER_INDEX]:
            result = Person.objects.get(
                    first_name=row[PL_ST_FIRST_NAME_INDEX],
                    last_name=row[PL_ST_LAST_NAME_INDEX],
                    gender=row[PL_ST_GENDER_INDEX],
            )
            result = result, False
    except ObjectDoesNotExist:
        if row[PL_ST_GENDER_INDEX]:
            result = Person.objects.get_or_create(
                    first_name=row[PL_ST_FIRST_NAME_INDEX],
                    last_name=row[PL_ST_LAST_NAME_INDEX],
                    gender=row[PL_ST_GENDER_INDEX],
            )
        else:
            result = Person.objects.get_or_create(
                    first_name=row[PL_ST_FIRST_NAME_INDEX],
                    last_name=row[PL_ST_LAST_NAME_INDEX]
            )
    return result


def create_or_fetch_team(pName, pDivision):
    result = Team.objects.get_or_create(
            name=pName,
            division=pDivision,
    )
    return result


def create_or_fetch_player_stadistic(pGame, pPlayer, row):
    result = None
    if row[PL_ST_PLAYER_TRIES_INDEX] and int(row[PL_ST_PLAYER_TRIES_INDEX]) > 0:
        result = PlayerStadistic.objects.get_or_create(
                game=pGame,
                player=pPlayer,
                points=row[PL_ST_PLAYER_TRIES_INDEX]
        )
    return result


def get_game_phase(pCategory, pRound, pNumber, create):
    get_round = pRound
    if get_round == '\xc2\xbc':
        get_round = '1/4'

    if create:
        result = GameRound.objects.get_or_create(
                category=pCategory,
                round=get_round,
                number_teams=pNumber
        )
    else:
        result = GameRound.objects.get(
                category=pCategory,
                round=get_round,
                number_teams=pNumber
        ), False
    return result


def create_game_tournament(pTournament, pLocal, pVisitor, row):
    game_phase, created = get_game_phase(row[TG_CATEGORY_INDEX],
                                         row[TG_PHASE_INDEX],
                                         row[TG_PHASE_TEAMS_INDEX],
                                         False)
    print('Found phase:\n', game_phase)

    if row[TG_FIELD_INDEX]:
        field, created = GameField.objects.get_or_create(name=row[TG_FIELD_INDEX])
        printCF(field, created)
    else:
        field = None

    if row[TG_TIME_INDEX]:
        get_time = row[TG_TIME_INDEX]
    else:
        get_time = None

    game = Game.objects.create(
            tournament=pTournament,
            local=pLocal,
            visitor=pVisitor,
            local_score=row[TG_LOCAL_TEAM_SCORE_INDEX],
            visitor_score=row[TG_VISITOR_TEAM_SCORE_INDEX],
            phase=game_phase,
            field=field,
            time=get_time
    )
    return game


def fetch_game_stadistic(pTournament, pLocal, pVisitor, row):
    game_phase = get_game_phase(row[PL_ST_GAME_CATEGORY_INDEX],
                                row[PL_ST_GAME_ROUND_INDEX],
                                row[PL_ST_PHASE_TEAMS_INDEX],
                                False)
    print('Found phase:\n', game_phase)

    try:
        # first try with given local and visitor teams and scores:
        get_game = Game.objects.get(
                tournament=pTournament.id,
                local=pLocal.id,
                visitor=pVisitor.id,
                local_score=row[PL_ST_LOCAL_TEAM_SCORE_INDEX],
                visitor_score=row[PL_ST_VISITOR_TEAM_SCORE_INDEX],
                phase=game_phase.id
        )
        return get_game
    except Game.DoesNotExist:
        # ignore excetion and go for a second try
        pass
    # second try changing local and visitor teams and scores:
    get_game = Game.objects.get(
            tournament=pTournament,
            visitor=pLocal,
            local=pVisitor,
            visitor_score=int(row[PL_ST_LOCAL_TEAM_SCORE_INDEX]),
            local_score=int(row[PL_ST_VISITOR_TEAM_SCORE_INDEX]),
            phase=game_phase
    )
    return get_game


def get_or_create_tournament(pName, pDivision):
    result = Tournament.objects.get_or_create(name=pName, division=pDivision)
    return result


def printCF(obj, created):
    if obj:
        if created:
            print('Created {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
        else:
            print('Found {:s}:\n {:s}'.format(obj.__class__.__name__, obj))
    else:
        print('ERROR\n')


def print_read_file_result(obj, created):
    if created:
        print('Created {:s}:\n'.format('aaa') + str(obj))
    else:
        print('Found {:s}:\n'.format('aaa') + str(obj))


def readTournamentStadisticRow(row):
    tournament = get_or_create_tournament(row[PL_ST_TOURNAMENT_INDEX], row[PL_ST_DIVISION_INDEX])
    printCF(tournament, False)

    get_team = Team.objects.get(name=row[PL_ST_TEAM_INDEX])
    printCF(get_team, False)

    get_person, created = create_or_fetch_person(row)
    printCF(get_person, created)

    get_player, created = Player.objects.get_or_create(
            person=get_person,
            team=get_team,
            number=row[PL_ST_NUMBER_INDEX]
    )
    printCF(get_player, created)

    if row[PL_ST_VISITOR_TEAM_SCORE_INDEX]:  # maybe only player insert.
        get_local_team = Team.objects.get(name=row[PL_ST_LOCAL_TEAM_INDEX])
        printCF(get_local_team, False)

        get_visitor_team = Team.objects.get(name=row[PL_ST_VISITOR_TEAM_INDEX])
        printCF(get_visitor_team, False)

        get_game = fetch_game_stadistic(tournament, get_local_team, get_visitor_team, row)
        printCF(get_game, False)

        get_player_stadistic, created = create_or_fetch_player_stadistic(
                get_game,
                get_player,
                row
        )
        printCF(get_player_stadistic, created)
    else:
        print('GameStadistic skipped: there is no scores for player: {:s}\n '.format(get_player))


def readTournamentGameRow(row):
    tournament, created = get_or_create_tournament(row[TG_TOURNAMENT_INDEX], row[TG_DIVISION_INDEX])
    # printCF(tournament, created)
    print_read_file_result(tournament, created)

    local_team, created = create_or_fetch_team(row[TG_LOCAL_TEAM_INDEX], row[TG_DIVISION_INDEX])
    # printCF(local_team, created)
    print_read_file_result(local_team, created)

    if created:
        add_team_to_tournament(tournament, local_team)

    visitor_team, created = create_or_fetch_team(row[TG_VISITOR_TEAM_INDEX], row[TG_DIVISION_INDEX])
    # printCF(visitor_team, created)
    print_read_file_result(visitor_team, created)

    if created:
        add_team_to_tournament(tournament, visitor_team)

    game = create_game_tournament(tournament, local_team, visitor_team, row)
    # printCF(game, True)
    print_read_file_result(game, True)


def readTournamentStadistic(file):
    print('\nStarting reading tournament stadistics from {:s}\n', file)
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if any(row):
                if row[0] == '####':
                    print('\n Forcef exit #### :)\n')
                    break
                print('\nRow to read:\n {:s}\n'.format(row))
                readTournamentStadisticRow(row)
    print('\nFinished reading tournament statistics...\n')


def read_tournament_games(file):
    print('\nStarting reading tournament games from {:s}\n'.format(file))
    with open(file, 'rt', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            if any(row):
                if row[0] == '####':
                    print('\n Force exit #### :)\n')
                    break
                # print('\nRow to read:\n {:s}\n'.format(row))
                csvgame = csvdata.CsvGame(row, None, None, None)
                CsvReader.print_row_to_read(csvgame)
                csv_reader = CsvReader("tournament")
                csv_reader.read_file(file, csvdata.CsvGame)
                readTournamentGameRow(row)
    print('\nFinished reading tournament games...\n')


def readPhases(file):
    print('\nStarting reading phases from {:s}\n'.format(file))
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if any(row):
                if row[0] == '####':
                    print('\n Forcef exit #### :)\n')
                    break
                print('\nRow to read:\n {:s}\n'.format(row))
                csvphase = CsvPhase(row)
                print(csvphase.to_csv_array())
                phase, created = get_game_phase(csvphase, True)
                printCF(phase, created)
    print('\nFinished reading phases...\n')


def readWC2015(fname):
    response = urllib2.urlopen(fname)
    html = response.read()
    print(html)


class CsvReader:
    (PHASE, TOURNAMENT, NTS_STADISTIC) = (0, 1, 2)

    def __init__(self, type):
        if type == self.PHASE or type == self.TOURNAMENT or type == self.NTS_STADISTIC:
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
        elif self._type == self.NTS_STADISTIC:
            result = csvdata.CsvNTSStadistic(row)
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
        elif self._type == self.NTS_STADISTIC and isinstance(csv_object, csvdata.CsvNTSStadistic):
            DjangoCsvFetcher.create_csv_nts_player_stadistic(csv_object)
        else:
            assert 0, "Wrong object to read: " + self._type

    def read_file(self, file, subclass):
        with open(file, 'rt', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            print('\nStarting reading {:n} from {:s}\n'.format(self._type, file))
            for row in reader:
                if any(row):
                    if row[0] == self._fexit:
                        print(self._exit_text)
                        break
                    self.print_row_to_read(row)
                    csv_object = self.get_csv_object(row)
                    self.create_django_object(csv_object)
        print('\nFinished reading {:s}...[0=PHASE, 1=TOURNAMENT, 2=NTS_STADISTIC]\n'.format(str(self._type)))

# reader = CsvReader(CsvReader.PHASE)
# reader.read_file('./player/data_files/csv/TPhases.csv', csvdata.CsvPhase)
# reader = CsvReader(CsvReader.TOURNAMENT)
# reader.read_file('./player/data_files/csv/TGames_WC2015_MX_RAW.csv', csvdata.CsvPhase)
# reader = CsvReader(CsvReader.NTS_STADISTIC)
# reader.read_file('./player/NTS-player-statistics.csv', csvdata.CsvNTSStadistic)
# read_tournament_games('./player/data_files/csv/TGames_WC2015_MO_RAW.csv')
# exit(0)
