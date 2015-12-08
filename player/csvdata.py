from datetime import datetime
import time

# PHASES_INDEXES
PH_PHASE_ROUND_INDEX = 0
PH_CATEGORY_INDEX = 1
PH_PHASE_TEAMS_INDEX = 2

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

# POSITION CONSTANTS CONVERSION
THIRD_POSITION = 'Third position'
FIFTH_POSITION = 'Fifth position'
SIXTH_POSITION = 'Sixth position'
SEVENTH_POSITION = 'Seventh position'
EIGHTH_POSITION = 'Eighth position'
NINTH_POSITION = 'Ninth position'
TENTH_POSITION = 'Tenth position'
ELEVENTH_POSITION = 'Eleventh position'
TWELFTH_POSITION = 'Twelfth position'
THIRTEENTH_POSITION = 'Thirteenth position'
FOURTEENTH_POSITION = 'Fourteenth position'
FIFTEENTH_POSITION = 'Fifteenth position'
SIXTEENTH_POSITION = 'Sixteenth position'
EIGHTEENTH_POSITION = 'Eighteenth position'
TWENTIETH_POSITION = 'Twentieth position'

# CONSTANTS DIRECTORIES
DATA_FILES = './data_files/'
RAW_FILES = DATA_FILES + 'raw/'
CSV_FILES = DATA_FILES + 'csv/'

# CONSTANTS FILE NAMES
GAME_PREFIX = 'TGames'
WC2015_MO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mens/'
WC2015_WO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/womens/'
WC2015_MXO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mixed/'
WC2015_MO_RAW = RAW_FILES + 'WC2015_MO_RAW.txt'
WC2015_WO_RAW = RAW_FILES + 'WC2015_WO_RAW.txt'
WC2015_MXO_RAW = RAW_FILES + 'WC2015_MX_RAW.txt'
WC2015_MO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_MO_RAW.csv'
WC2015_WO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_WO_RAW.csv'
WC2015_MXO_CSV = CSV_FILES + GAME_PREFIX + '_WC2015_MX_RAW.csv'

# CONSTANTS ALGORITHMS
WC2015_RE_GROUPS = '[Pool [A|B|C|D|E|F]|Division [1|2|3]'
WC2015_RE_FINALS = '[Grand Final|Bronze|Playoff ]'


class CsvNTSStadistic:
    def __init__(self, row):
        self._tournament_name = row[PL_ST_TOURNAMENT_INDEX]
        self._division = row[PL_ST_DIVISION_INDEX]
        self._team = row[PL_ST_TEAM_INDEX]
        self._number = row[PL_ST_NUMBER_INDEX]
        self._first_name = row[PL_ST_FIRST_NAME_INDEX]
        self._last_name = row[PL_ST_LAST_NAME_INDEX]
        self._gender = row[PL_ST_GENDER_INDEX]
        self._tries = row[PL_ST_PLAYER_TRIES_INDEX]
        self._local = row[PL_ST_LOCAL_TEAM_INDEX]
        self._local_score = row[PL_ST_LOCAL_TEAM_SCORE_INDEX]
        self._visitor_score = row[PL_ST_VISITOR_TEAM_SCORE_INDEX]
        self._visitor = row[PL_ST_VISITOR_TEAM_INDEX]
        self._category = row[PL_ST_GAME_CATEGORY_INDEX]
        self._round = row[PL_ST_GAME_ROUND_INDEX]
        self._team_numbers = row[PL_ST_PHASE_TEAMS_INDEX]

    @property
    def tournament_name(self):
        return self._tournament_name

    @tournament_name.setter
    def tournament_name(self, tournament_name):
        self._tournament_name = tournament_name

    @property
    def division(self):
        return self._division

    @division.setter
    def division(self, division):
        self._division = division

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, team):
        self._team = team

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def tries(self):
        return self._tries

    @tries.setter
    def tries(self, tries):
        self._tries = tries

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def local_score(self):
        return self._local_score

    @local_score.setter
    def local_score(self, local_score):
        self._local_score = local_score

    @property
    def visitor_score(self):
        return self._visitor_score

    @visitor_score.setter
    def visitor_score(self, visitor_score):
        self._visitor_score = visitor_score

    @property
    def visitor(self):
        return self._visitor

    @visitor.setter
    def visitor(self, visitor):
        self._visitor = visitor

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def round(self):
        #print(self._round.encode('UTF-8'))
        if self._round.encode('UTF-8') == b'\xc2\xbc':
            result = '1/4'
        else:
            result = self._round
        return result

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def team_numbers(self):
        return self._team_numbers

    @team_numbers.setter
    def team_numbers(self, team_numbers):
        self._team_numbers = team_numbers

    def to_csv_array(self):
        result = list(range(15))
        result[PL_ST_TOURNAMENT_INDEX] = self._category
        result[PL_ST_DIVISION_INDEX] = self._division
        result[PL_ST_TEAM_INDEX] = self._team
        result[PL_ST_NUMBER_INDEX] = self._number
        result[PL_ST_FIRST_NAME_INDEX] = self._first_name
        result[PL_ST_LAST_NAME_INDEX] = self._last_name
        result[PL_ST_GENDER_INDEX] = self._gender
        result[PL_ST_PLAYER_TRIES_INDEX] = self._tries
        result[PL_ST_LOCAL_TEAM_INDEX] = self._local
        result[PL_ST_LOCAL_TEAM_SCORE_INDEX] = self._local_score
        result[PL_ST_VISITOR_TEAM_SCORE_INDEX] = self._visitor_score
        result[PL_ST_VISITOR_TEAM_INDEX] = self._visitor
        result[PL_ST_GAME_CATEGORY_INDEX] = self._category
        result[PL_ST_GAME_ROUND_INDEX] = self._round
        result[PL_ST_PHASE_TEAMS_INDEX] = self._teams
        return result

    def to_csv_game(self):
        pass


class CsvPhase:
    def __init__(self, row):
        self._category = row[PH_CATEGORY_INDEX]
        self._round = row[PH_PHASE_ROUND_INDEX]
        self._teams = row[PH_PHASE_TEAMS_INDEX]

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def round(self):
        if self._round.encode('UTF-8') == b'\xc2\xbc':
            result = '1/4'
        else:
            result = self._round
        return result

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, teams):
        self._teams = teams

    def to_csv_array(self):
        result = list(range(3))
        result[PH_CATEGORY_INDEX] = self._category
        result[PH_PHASE_ROUND_INDEX] = self._round
        result[PH_PHASE_TEAMS_INDEX] = self._teams
        return result


class FitGame:
    def __init__(self, game, round=None, finals=None, nteams=None, date=None, time=None,
                 field=None, local=None, local_score=None, visitor_score=None, visitor=None):
        if game:
            self._round = game[0]
            self._finals = game[2]
            self._nteams = game[1]
            self._date = time.strftime("%m/%d/%y", game[3])
            self._time = time.strftime("%H:%M", game[3])
            self._timedate = game[3]
            self._field = game[4]
            self._local = game[5]
            self._local_score = game[6]
            self._visitor_score = game[7]
            self._visitor = game[8]
        else:
            self._round = round
            self._finals = finals
            self._nteams = nteams
            self._date = date
            self._time = time
            self._field = field
            self._local = local
            self._local_score = local_score
            self._visitor_score = visitor_score
            self._visitor = visitor

    def to_array(self):
        result = list(range(8))
        result[0] = self.round
        result[1] = self.nteams
        result[2] = self.finals
        result[3] = None
        result[4] = self.field
        result[5] = self.local
        result[6] = self.local_score
        result[7] = self.visitor_score
        result[8] = self.visitor

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def finals(self):
        return self._finals

    @finals.setter
    def finals(self, finals):
        self._finals = finals

    @property
    def nteams(self):
        return self._nteams

    @nteams.setter
    def nteams(self, nteams):
        self._nteams = nteams

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, field):
        self._field = field

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def visitor(self):
        return self._visitor

    @visitor.setter
    def visitor(self, visitor):
        self._visitor = visitor

    @property
    def local_score(self):
        return self._local_score

    @local_score.setter
    def local_score(self, local_score):
        self._local_score = local_score

    @property
    def visitor_score(self):
        return self._visitor_score

    @visitor_score.setter
    def visitor_score(self, visitor_score):
        self._visitor_score = visitor_score


class CsvGame(FitGame):

    def __init__(self, row, game, tournament_name, division):
        if row is None:
            super(FitGame, self).__init__(None, game.round, game.finals, game.nteams, game.date, game.time, game.field,
                                          game.local, game.local_score, game.visitor_score, game.visitor)

            self._tournament_name = tournament_name
            self._division = division
            self._category = 'Gold'

            if game.round == 'Division 2':
                self._category = 'Silver'
            elif game.round == 'Division 3':
                self._category = 'Bronze'
            else:
                self._category = 'Gold'

            if 'Division' in game.round:
                self._round = 'Division'
            elif 'finals' == game.round:
                self._round = game.finals
                self._round = self._round.replace('Grand Final', 'Final', 1)
                self._round = self._round.replace('Playoff 5th/6th', FIFTH_POSITION, 1)
                self._round = self._round.replace('Playoff 6th/7th', SIXTH_POSITION, 1)
                self._round = self._round.replace('Playoff 7th/8th', SEVENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 8th/9th', EIGHTH_POSITION, 1)
                self._round = self._round.replace('Playoff 9th/10th', NINTH_POSITION, 1)
                self._round = self._round.replace('Playoff 10th/11th', TENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 11th/12th', ELEVENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 12th/13th', TWELFTH_POSITION, 1)
                self._round = self._round.replace('Playoff 13th/14th', THIRTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 14th/15th', FOURTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 15th/16th', FIFTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 16th/17th', SIXTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 18th/19th', EIGHTEENTH_POSITION, 1)
                self._round = self._round.replace('Playoff 20th/21st', TWENTIETH_POSITION, 1)
                self._round = self._round.replace('Bronze', THIRD_POSITION, 1)
            else:
                self._round = game.round
        else:
            super(CsvGame, self).__init__(None, row[TG_PHASE_INDEX], None, row[TG_PHASE_TEAMS_INDEX],
                                          row[TG_DATE_INDEX], row[TG_TIME_INDEX], row[TG_FIELD_INDEX],
                                          row[TG_LOCAL_TEAM_INDEX], row[TG_LOCAL_TEAM_SCORE_INDEX],
                                          row[TG_VISITOR_TEAM_SCORE_INDEX], row[TG_VISITOR_TEAM_INDEX])
            self._tournament_name = row[TG_TOURNAMENT_INDEX]
            self._division = row[TG_DIVISION_INDEX]
            self._category = row[TG_CATEGORY_INDEX]

    @property
    def tournament_name(self):
        return self._tournament_name

    @tournament_name.setter
    def tournament_name(self, tournament_name):
        self._tournament_name = tournament_name

    @property
    def division(self):
        return self._division

    @division.setter
    def division(self, division):
        self._division = division

    @property
    def round(self):
        return self._round

    @round.setter
    def round(self, round):
        self._round = round

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    def to_csv_array(self):
        result = list(range(13))
        result[TG_TOURNAMENT_INDEX] = self._tournament_name
        result[TG_DIVISION_INDEX] = self._division
        result[TG_DATE_INDEX] = self.date
        result[TG_TIME_INDEX] = self.time
        result[TG_FIELD_INDEX] = self._field
        result[TG_PHASE_INDEX] = self._round
        result[TG_CATEGORY_INDEX] = self._category
        result[TG_PHASE_TEAMS_INDEX] = self._nteams
        result[8] = 'xx'
        result[TG_LOCAL_TEAM_INDEX] = self._local
        result[TG_LOCAL_TEAM_SCORE_INDEX] = self._local_score
        result[TG_VISITOR_TEAM_SCORE_INDEX] = self._visitor_score
        result[TG_VISITOR_TEAM_INDEX] = self._visitor
        return result

    def __str__(self):
        return self.to_csv_array().__str__()
