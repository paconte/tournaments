import csv
import logging
import os.path
import re
import time

import requests
from bs4 import BeautifulSoup

from player import csvdata

# CONSTANTS
GAME_PREFIX = 'TGames'

WC2015_RE_GROUPS = '[Pool [A|B|C|D|E|F]|Division [1|2|3]'
WC2015_RE_FINALS = '[Grand Final|Bronze|Playoff ]'

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

# FILES CONTANTS
WC2015_MO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mens/'
WC2015_WO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/womens/'
WC2015_MXO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mixed/'

WC2015_MO_RAW = csvdata.RAW_GAMES_FILES + 'WC2015_MO_RAW.txt'
WC2015_WO_RAW = csvdata.RAW_GAMES_FILES + 'WC2015_WO_RAW.txt'
WC2015_MXO_RAW = csvdata.RAW_GAMES_FILES + 'WC2015_MX_RAW.txt'

WC2015_MO_CSV = csvdata.CSV_FILES + GAME_PREFIX + '_WC2015_MO_RAW.csv'
WC2015_WO_CSV = csvdata.CSV_FILES + GAME_PREFIX + '_WC2015_WO_RAW.csv'
WC2015_MXO_CSV = csvdata.CSV_FILES + GAME_PREFIX + '_WC2015_MX_RAW.csv'

WC2015_WO_FOX_CSV = csvdata.CSV_FILES + GAME_PREFIX + '_WC2015_WO_FOX.csv'
WC2015_MO_FOX_CSV = csvdata.CSV_FILES + GAME_PREFIX + '_WC2015_WO_FOX.csv'
WC2015_MXO_FOX_CSV = csvdata.CSV_FILES + GAME_PREFIX + '_WC2015_WO_FOX.csv'

WC2015_MO_GENERATED_FILE = './WC2015_MO_GENERATED.csv'
WC2015_WO_GENERATED_FILE = './WC2015_WO_GENERATED.csv'
WC2015_MX_GENERATED_FILE = './WC2015_MX_GENERATED.csv'
WC2015_MO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mens/'
WC2015_WO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/womens/'
WC2015_MX_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mixed/'
WC2015_MO_FILE = './WC2015_MO.txt'
WC2015_WO_FILE = './WC2015_WO.txt'
WC2015_MX_FILE = './WC2015_MX.txt'

remote_files_WC_2015_WO_FX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=11&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=12&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=13&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=14&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=21&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=22&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=1031&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360318-0&pool=1032&action=ROUND&round=-1']

remote_files_WC_2015_MO_FX = [
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=11&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=12&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=13&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=14&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=21&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=22&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=1031&action=ROUND&round=-1',
    'http://www.foxsportspulse.com/comp_info.cgi?client=1-9035-0-360314-0&pool=1032&action=ROUND&round=-1']

local_files_WC_2015_MO_FX = [csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLA.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLB.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLC.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_POOLD.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_DIVONE.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_DIVTWO.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_CHAMPIONSHIP.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_MO_FOX_PLATE.html']

local_files_WC_2015_WO_FX = [csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLA.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLB.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLC.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_POOLD.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_DIVONE.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_DIVTWO.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_CHAMPIONSHIP.html',
                             csvdata.RAW_GAMES_FILES + 'WC2015_WO_FOX_PLATE.html']

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class FitGamesManager:
    def __init__(self, tournament, division, year):
        if tournament == 'WC' and year == 2015 and division == 'MO':
            self.url = WC2015_MO_URL
            self.raw = WC2015_MO_RAW
            self.csv = WC2015_MO_CSV
            self.t_name = 'World Cup 2015'
        elif tournament == 'WC' and year == 2015 and division == 'WO':
            self.url = WC2015_WO_URL
            self.raw = WC2015_WO_RAW
            self.csv = WC2015_WO_CSV
            self.t_name = 'World Cup 2015'
        elif tournament == 'WC' and year == 2015 and division == 'MXO':
            self.url = WC2015_MXO_URL
            self.raw = WC2015_MXO_RAW
            self.csv = WC2015_MXO_CSV
            self.t_name = 'World Cup 2015'
        else:
            assert 0, "Illegal arguments: %s %s %s" % (tournament, division, year)
        self.t_division = division

    def download_raw_file(self, force=False):
        exists = os.path.isfile(self.raw)
        if force or not exists:
            logging.debug('Downloading file: %s' % self.url)
            page = requests.get(self.url)
            with open(self.raw, 'wb') as code:
                code.write(page.content)
            logging.debug('Downloaded file to: %s' % self.raw)
        else:
            logging.debug('File already exists, no need to download it.')

    def write_csv_games(self):
        with open(self.csv, 'w') as csvfile:
            spamwriter = csv.writer(csvfile,
                                    delimiter=';',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL
                                    )
            logging.debug('Writing CSV file: %s' % (self.csv))
            for game in self.csv_games:
                spamwriter.writerow(game.to_csv_array())
            logging.debug('Done writing CSV file: %s' % (self.csv))

    def print_csv_games(self):
        for game in self.csv_games:
            print('{}\n'.format(game))

    def len_csv_games(self):
        # print 'len(csv_games) = %s' % len(self.csv_games)
        print('len(csv_games) = {}'.format(len(self.csv_games)))

    def games_to_csv_array(self, games):
        result = []
        for game in games:
            g1 = csvdata.FitGame(game)
            g = csvdata.CsvGame(None, g1, self.t_name, self.t_division)
            result.append(g)
        return result

    def find_group_position(self, groups, position):
        if position == 1:
            if re.match('Pool [A|B|C|D|E|F]', groups[0]):
                result = groups[0]
            elif re.match('Pool [A|B|C|D|E|F]', groups[1]):
                result = groups[1]
            else:
                raise Exception('Illegal Argument')
        elif position == 2:
            if re.match('Division [1|2|3]', groups[0]):
                result = groups[0]
            elif re.match('Division [1|2|3]', groups[1]):
                result = groups[1]
            else:
                raise Exception('Illegal Argument')
        else:
            raise Exception('Illegal Argument')

        return result

    def find_game_groups(self, local, visitor, groups):
        aux = dict()
        result = []
        for key, teams in groups.items():
            exists_local = False
            exists_visitor = False
            for team in teams:
                exists_local = True if team == local else exists_local
                exists_visitor = True if team == visitor else exists_visitor
                if exists_local and exists_visitor:
                    aux[key] = ''
        assert len(aux) <= 2, "Find more than 2 groups: %s" % (aux)
        for key in aux.keys():
            result.append(key)
        return result

    def get_group_size(self, key, groups):
        return len(groups.get(key))

    def assign_games_to_groups(self, games, groups):
        result = []
        multiple_choice_list = []
        for game in games:
            local = game[3]
            visitor = game[6]
            if re.match(WC2015_RE_FINALS, game[0]):
                assigned_group = 'finals'
                nteams = 2
            else:
                possible_groups = self.find_game_groups(local, visitor, groups)
                if len(possible_groups) > 1:
                    if ([local, visitor] not in multiple_choice_list) or ([visitor, local] not in multiple_choice_list):
                        assigned_group = self.find_group_position(possible_groups, 1)
                        multiple_choice_list.append([local, visitor])
                        multiple_choice_list.append([visitor, local])
                    else:
                        assigned_group = self.find_group_position(possible_groups, 2)
                else:
                    assigned_group = possible_groups[0]
                nteams = self.get_group_size(assigned_group, groups)
            game.insert(0, assigned_group)
            game.insert(1, nteams)
        return games

    def extract_raw_groups(self, soup):
        pools = dict()
        for row0 in soup.findAll('table', {"class": "info-table"}):
            pool = []
            for row1 in row0.tbody.findAll(['tr', 'td']):
                if row1.find('th', text=re.compile(WC2015_RE_GROUPS)):
                    pool_name = row1.find('th', text=re.compile(WC2015_RE_GROUPS)).get_text()
                for row2 in row1.findAll('td', {"class": "team"}):
                    for row3 in row2.find('span').contents:
                        pool.append(row3)
                        pools[pool_name] = pool
        return pools

    def extract_raw_games(self, soup):
        games = []
        for row1 in soup.findAll('table', {"class": "round-table"}):
            game_date = row1.previous_sibling.previous_sibling.string
            for row2 in row1.findAll('tr'):
                game = list(range(7))
                if row2.find('strong', {"class": "round"}):
                    current_round = row2.find('strong', {"class": "round"}).contents[0].strip()
                game[0] = current_round
                game_time = row2.find('td', {"class": "time"}).find('span').contents[0]
                game[1] = self.convert_time(game_time, game_date)
                # game[1] = datetime(*game[1][:6]).isoformat()
                game[2] = row2.find('td', {"class": "field"}).find('span').contents[0]
                game[3] = row2.find('td', {"class": "home"}).find('span').contents[0]
                i = 4
                for score in row2.findAll('td', {"class": "score"}):
                    game[i] = score.contents[0]
                    i += 1
                    game[6] = row2.find('td', {"class": "away"}).find('span').contents[0]
                games.append(game)
        return games

    def rep1(self, n):
        if int(n.group(0)) < 10:
            result = str(n.group(0)).zfill(2)
        else:
            result = str(n.group(0))
        return result

    def convert_time(self, arg1, arg2):
        if "a.m" in arg1:
            ntime = arg1.replace("a.m.", "AM")
        elif "p.m." in arg1:
            ntime = arg1.replace("p.m.", "PM")
        ndate = re.sub('\d+', self.rep1, arg2, 1)
        final_date = ndate + ' ' + ntime
        result = time.strptime(final_date, '%d %b %Y %I:%M %p')
        return result

    def create_csv_file(self):
        f = open(self.raw, 'r')
        soup = BeautifulSoup(f, "lxml")
        raw_games = self.extract_raw_games(soup)
        raw_groups = self.extract_raw_groups(soup)
        raw_sorted_games = self.assign_games_to_groups(raw_games, raw_groups)
        self.csv_games = self.games_to_csv_array(raw_sorted_games)
        self.write_csv_games()


def download_file(src, dst):
    logger.debug('Downloading remote file: %s\nTo local file %s', src, dst)
    page = requests.get(src)
    with open(dst, 'wb') as code:
        code.write(page.content)
    logger.debug('Download complete')


def find_group_position(groups, position):
    if position == 1:
        if re.match('Pool [A|B|C|D|E|F]', groups[0]):
            result = groups[0]
        elif re.match('Pool [A|B|C|D|E|F]', groups[1]):
            result = groups[1]
        else:
            raise Exception('Illegal Argument')
    elif position == 2:
        if re.match('Division [1|2|3]', groups[0]):
            result = groups[0]
        elif re.match('Division [1|2|3]', groups[1]):
            result = groups[1]
        else:
            raise Exception('Illegal Argument')
    else:
        raise Exception('Illegal Argument')

    return result


def find_game_groups(local, visitor, groups):
    result = []
    for key, teams in groups.iteritems():
        exists_local = False
        exists_visitor = False
        for team in teams:
            exists_local = True if team == local else exists_local
            exists_visitor = True if team == visitor else exists_visitor
        if exists_local and exists_visitor:
            result.append(key)
    return result


def get_group_size(key, groups):
    return len(groups.get(key))


def assign_games_to_groups(games, groups):
    result = []
    multiple_choice_list = []
    for game in games:
        local = game[3]
        visitor = game[6]
        if (re.match(WC2015_RE_FINALS, game[0])):
            assigned_group = 'finals'
            nteams = 2
        else:
            possible_groups = find_game_groups(local, visitor, groups)
            if len(possible_groups) > 1:
                if (([local, visitor] not in multiple_choice_list)
                    or ([visitor, local] not in multiple_choice_list)):
                    assigned_group = find_group_position(possible_groups, 1)
                    multiple_choice_list.append([local, visitor])
                    multiple_choice_list.append([visitor, local])
                else:
                    assigned_group = find_group_position(possible_groups, 2)
            else:
                assigned_group = possible_groups[0]
            nteams = get_group_size(assigned_group, groups)
        game.insert(0, assigned_group)
        game.insert(1, nteams)
    return games


def extract_groups_fit(soup):
    pools = dict()
    for row0 in soup.findAll('table', {"class": "info-table"}):
        pool = []
        for row1 in row0.tbody.findAll(['tr', 'td']):
            if row1.find('th', text=re.compile(WC2015_RE_GROUPS)):
                pool_name = row1.find('th', text=re.compile(WC2015_RE_GROUPS)).get_text()
            for row2 in row1.findAll('td', {"class": "team"}):
                for row3 in row2.find('span').contents:
                    pool.append(row3)
                    pools[pool_name] = pool
    return pools


def extract_games_fit(soup):
    games = []
    for row1 in soup.findAll('table', {"class": "round-table"}):
        game_date = row1.previous_sibling.previous_sibling.string
        for row2 in row1.findAll('tr'):
            game = range(7)
            if row2.find('strong', {"class": "round"}):
                current_round = row2.find('strong', {"class": "round"}).contents[0].strip()
            game[0] = current_round
            game_time = row2.find('td', {"class": "time"}).find('span').contents[0]
            game[1] = convert_time(game_time, game_date)
            #            game[1] = datetime(*game[1][:6]).isoformat()
            game[2] = row2.find('td', {"class": "field"}).find('span').contents[0]
            game[3] = row2.find('td', {"class": "home"}).find('span').contents[0]
            i = 4
            for score in row2.findAll('td', {"class": "score"}):
                game[i] = score.contents[0]
                i += 1
                game[6] = row2.find('td', {"class": "away"}).find('span').contents[0]
            games.append(game)
    return games


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


def rep1(n):
    if int(n.group(0)) < 10:
        result = str(n.group(0)).zfill(2)
    else:
        result = str(n.group(0))
    return result


def convert_fox_time(arg, year):
    arg = arg.replace(u'\xa0', ' ')
    aux = arg.split(' / ', maxsplit=1)
    result = time.strptime(aux[0] + " " + aux[1] + " " + str(year), "%I:%M %p %a %d %b %Y")
    return result


def convert_time(arg1, arg2):
    if "a.m" in arg1:
        ntime = arg1.replace("a.m.", "AM")
    elif "p.m." in arg1:
        ntime = arg1.replace("p.m.", "PM")
    ndate = re.sub('\d+', rep1, arg2, 1)
    final_date = ndate + ' ' + ntime
    result = time.strptime(final_date, '%d %b %Y %I:%M %p')
    return result


def get_game_nteams(game): return game[1]


def get_game_date(game): return time.strftime("%m/%d/%y", game[3])


def get_game_time(game): return time.strftime("%H:%M", game[3])


def get_game_field(game): return game[4]


def get_game_local(game): return game[5]


def get_game_local_score(game): return game[6]


def get_game_visitor_score(game): return game[7]


def get_game_visitor(game): return game[8]


def get_game_round(game):
    if 'Division' in game[0]:
        result = 'Division'
    elif 'finals' in game[0]:
        result = game[2]
        result = result.replace('Grand Final', 'Final', 1)
        result = result.replace('Playoff 5th/6th', FIFTH_POSITION, 1)
        result = result.replace('Playoff 6th/7th', SIXTH_POSITION, 1)
        result = result.replace('Playoff 7th/8th', SEVENTH_POSITION, 1)
        result = result.replace('Playoff 8th/9th', EIGHTH_POSITION, 1)
        result = result.replace('Playoff 9th/10th', NINTH_POSITION, 1)
        result = result.replace('Playoff 10th/11th', TENTH_POSITION, 1)
        result = result.replace('Playoff 11th/12th', ELEVENTH_POSITION, 1)
        result = result.replace('Playoff 12th/13th', TWELFTH_POSITION, 1)
        result = result.replace('Playoff 13th/14th', THIRTEENTH_POSITION, 1)
        result = result.replace('Playoff 14th/15th', FOURTEENTH_POSITION, 1)
        result = result.replace('Playoff 15th/16th', FIFTEENTH_POSITION, 1)
        result = result.replace('Playoff 16th/17th', SIXTEENTH_POSITION, 1)
        result = result.replace('Playoff 18th/19th', EIGHTEENTH_POSITION, 1)
        result = result.replace('Playoff 20th/21st', TWENTIETH_POSITION, 1)
        result = result.replace('Bronze', THIRD_POSITION, 1)
    else:
        result = game[0]
    return result


def get_game_category(game):
    if game[0] == 'Division 2':
        result = 'Silver'
    else:
        result = 'Gold'
    return result


def games_to_csv_array(games, t_name, t_division):
    results = []
    for game in games:
        result = range(13)
        result[0] = t_name
        result[1] = t_division
        result[2] = get_game_date(game)
        result[3] = get_game_time(game)
        result[4] = get_game_field(game)
        result[5] = get_game_round(game)
        result[6] = get_game_category(game)
        result[7] = get_game_nteams(game)
        result[8] = 'xx'
        result[9] = get_game_local(game)
        result[10] = get_game_local_score(game)
        result[11] = get_game_visitor_score(game)
        result[12] = get_game_visitor(game)
        results.append(result)
    return results


def write_csv(games, fname):
    with open(fname, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter=';',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL
                                )
        for game in games:
            spamwriter.writerow(game)


class FoxGamesManager:
    GAME_INDEX_STATISTIC = 10
    (WC_2015_MO_FOX, WC_2015_WO_FOX, WC_2015_MXO_FOX) = (0, 1, 2)

    def __init__(self, tournament):
        self._games = []
        self._fox_games = []
        self._csv_games = []
        self._csv_stats = []
        if tournament == self.WC_2015_MO_FOX:
            self._root_website = 'http://www.foxsportspulse.com/'
            self._remote_files = remote_files_WC_2015_MO_FX
            self._local_files = local_files_WC_2015_MO_FX
            self._year = 2015
            self._tournament_name = 'World Cup 2015'
            self._tournament_division = 'MO'
        elif tournament == self.WC_2015_WO_FOX:
            self._root_website = 'http://www.foxsportspulse.com/'
            self._remote_files = remote_files_WC_2015_WO_FX
            self._local_files = local_files_WC_2015_WO_FX
            self._tournament_name = 'World Cup 2015'
            self._tournament_division = 'WO'
            self._year = 2015
        elif tournament == self.WC_2015_MXO_FOX:
            self._root_website = 'http://www.foxsportspulse.com/'
            self._year = 2015
            self._tournament_name = 'World Cup 2015'
            self._tournament_division = 'MXO'
            raise Exception("Tournament not supported.")
            # remote_files = remote_files_WC_2015_MXO_FX
            # local_files = local_files_WC_2015_MXO_FX
        else:
            raise Exception("Tournament not supported.")

    def download_games_files(self):
        for i in range(0, len(self._remote_files)):
            download_file(self._remote_files[i], self._local_files[i])

    def get_game_statistic_file_to_save(self, game):
        destination = self._tournament_name + '-' + str(self._year) + '-' + self._tournament_division + '-' + str(
                game[0]) + '-' + str(game[1]) + '-' + str(game[2]) + '-' + strftime("%m/%d/%y-%H:%M",
                                                                                    game[3]) + '-' + str(
                game[4]) + '-' + str(game[5]) + '-' + str(game[6]) + '-' + str(game[7]) + '-' + str(game[8]) + '.html'
        destination = destination.replace(' ', '')
        destination = destination.replace('/', '-')
        return csvdata.RAW_STATS_FILES + destination

    def download_games_statistics(self):
        if len(self._web_games) > 0:
            for game in self._web_games:
                destination = self.get_game_statistic_file_to_save(game)
                download_file(self._root_website + game[self.GAME_INDEX_STATISTIC], destination)

    def extract_raw_games(self):
        self._fox_games = []
        for i in range(0, len(self._local_files)):
            f = open(self._local_files[i], 'r')
            soup = BeautifulSoup(f)
            self._fox_games.extend(self.extract_games_fox(soup))

    def extract_statistics(self):
        if os.path.exists(csvdata.RAW_STATS_FILES) and os.path.isdir(csvdata.RAW_STATS_FILES):
            self._csv_stats = []
            for filename in os.listdir(csvdata.RAW_STATS_FILES):
                f = open(csvdata.RAW_STATS_FILES + filename, 'r')
                soup = BeautifulSoup(f)
                self.extract_game_statistic_fox(soup, filename)
        else:
            print('The directory %s does not exists.' % csvdata.RAW_STATS_FILES)
            logger.debug('The directory %s does not exists.', csvdata.RAW_STATS_FILES)

    def extract_games_fox(self, soup):
        result = []

        phase = soup.find(class_="compoptions comppage comppools").find(class_="fixoptions").find(
                class_="buttons active").contents[0]

        if phase in ['Championship', 'Plate', 'Division One Finals', 'Division Two Finals (Plate)',
                     'DIVISION THREE FINALS (BOWL)', 'PLAYOFF GAMES']:
            round = 'UNKNOWN'
            category = 'GOLD'
        elif 'Pool' in phase:
            round = phase
            category = 'GOLD'
        elif phase == 'Division One':
            round = 'DIVISION'
            category = 'GOLD'
        elif phase == 'Division Two':
            round = 'DIVISION'
            category = 'SILVER'
        elif phase == 'Division Three':
            round = 'DIVISION'
            category = 'BRONZE'
        else:
            print('Problem with the phase = %s' % phase)
            raise Exception('The phase is not supported')

        team_names = {}
        for row1 in soup.findAll(class_="all-fixture-wrap stacked-wide"):
            if round == 'UNKNOWN':
                round = row1.find(class_="match-name").contents[0]
            for row2 in row1.findAll(class_="match-wrap sport-5 fixturerow "):
                if row2.find(class_="match-name"):
                    round = row2.find(class_="match-name").contents[0]
                link = row2.find(class_="match-centre-link").find("a", href=True)
                local_team = row2.find(class_="home-team-name").find("a").contents[0]
                local_score = row2.find(class_="home-team-score").contents[0]
                visitor_team = row2.find(class_="away-team-name").find("a").contents[0]
                visitor_score = row2.find(class_="away-team-score").contents[0]
                time_date = row2.find(class_="match-time").contents[0]
                time_st = convert_fox_time(time_date, self._year)
                field = row2.find(class_="match-venue").find("a").contents[0]
                team_names[local_team] = None
                team_names[visitor_team] = None

                date = time.strftime("%m/%d/%y", time_st)
                t = time.strftime("%H:%M", time_st)

                game = list(range(11))
                game[0] = date
                game[1] = t
                game[2] = field
                game[3] = round
                game[4] = category
                #                game[5] = n_teams
                game[6] = local_team
                game[7] = local_score
                game[8] = visitor_score
                game[9] = visitor_team
                game[self.GAME_INDEX_STATISTIC] = link['href']
                result.append(game)
                print("%s - %s - %s - %s %s - %s %s - %s %s" % (
                    round, category, field, date, t, local_team, local_score, visitor_score, visitor_team))

        n_teams = len(team_names)
        for game in result:
            game[5] = n_teams

        return result

    def convert_fox_games_to_csv_games(self):
        self._csv_games = []
        for fgame in self._fox_games:
            csvgame = csvdata.CsvGame.from_scratch(self._tournament_name, self._tournament_division, fgame[0], fgame[1],
                                                   fgame[2], fgame[3], fgame[4], fgame[5], fgame[6], fgame[7], fgame[8],
                                                   fgame[9])
            self._csv_games.append(csvgame)

    def extract_game_statistic_fox(self, soup, filename):
        # ['WorldCup', '2015', 'WO', 'DIVISION', 'GOLD', '7', '05', '02', '15', '17', '00', 'Field9', 'England', '4', '5', 'Japan', 'html']
        filename_parts = re.split('\W+', filename)
        category = filename_parts[3]
        round = filename_parts[4]
        team_numbers = filename_parts[5]

        scores = soup.findAll(class_="big-score")
        local_score = scores[0].contents[0]
        visitor_score = scores[1].contents[0]

        local_stats = soup.find(class_="playerMatchStats").find(id="team-1-player-stats-wrap")
        local = local_stats.find("table", {"class": "tableClass stats"}).find(class_="tableTitle").find(
                'h4').contents[0]

        visitor_stats = soup.find(class_="playerMatchStats").find(id="team-2-player-stats-wrap")
        visitor = visitor_stats.find("table", {"class": "tableClass stats"}).find(class_="tableTitle").find(
                'h4').contents[0]

        # ignore the first element of the table[1:]!!
        for tr in local_stats.find("table", {"class": "tableClass stats"}).findAll('tr')[1:]:
            tds = tr.findAll('td')
            number = tds[0].contents[0]
            # only one first_name, the rest is last_name TODO: use some stats to separate properly?
            name = tds[1].find(class_="playerdetail resultlink").contents[0].split(" ", 1)
            first_name = name[0]
            last_name = name[1]
            tries = tds[2].contents[0]
            statistic = csvdata.CsvNTSStadistic(
                    None, self._tournament_name, self._tournament_division, local, number, first_name, last_name, None,
                    tries, local, local_score, visitor_score, visitor, category, round, team_numbers)
            self._csv_stats.append(statistic)

        for tr in visitor_stats.find("table", {"class": "tableClass stats"}).findAll('tr')[1:]:
            tds = tr.findAll('td')
            number = tds[0].contents[0]
            # only one first_name, the rest is last_name TODO: use some stats to separate properly?
            name = tds[1].find(class_="playerdetail resultlink").contents[0].split(" ", 1)
            first_name = name[0]
            last_name = name[1]
            tries = tds[2].contents[0]
            statistic = csvdata.CsvNTSStadistic(
                    None, self._tournament_name, self._tournament_division, visitor, number, first_name, last_name,
                    None, tries, local, local_score, visitor_score, visitor, category, round, team_numbers)
            self._csv_stats.append(statistic)

    def get_csv_games(self):
        return self._csv_games

    def get_csv_statistics(self):
        return self._csv_stats


class CsvWriter:
    (WC_2015_MO_GAMES_FOX, WC_2015_WO_GAMES_FOX, WC_2015_MXO_GAMES_FOX,
     WC_2015_MO_GAMES_FIT, WC_2015_WO_GAMES_FIT, WC_2015_MXO_GAMES_FIT,
     WC_2015_MO_STATS_FOX, WC_2015_WO_STATS_FOX, WC_2015_MXO_STATS_FOX) = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    def __init__(self, type):
        if type == self.WC_2015_MO_GAMES_FOX:
            self._filename = 'WC_2015_MO_GAMES_FOX'
        elif type == self.WC_2015_WO_GAMES_FOX:
            self._filename = 'WC_2015_WO_GAMES_FOX'
        elif type == self.WC_2015_MXO_GAMES_FOX:
            self._filename = 'WC_2015_MXO_GAMES_FOX'
        elif type == self.WC_2015_MO_GAMES_FIT:
            self._filename = 'WC_2015_MO_GAMES_FIT'
        elif type == self.WC_2015_WO_GAMES_FIT:
            self._filename = 'WC_2015_WO_GAMES_FIT'
        elif type == self.WC_2015_MXO_GAMES_FIT:
            self._filename = 'WC_2015_MXO_GAMES_FIT'
        elif type == self.WC_2015_MO_STATS_FOX:
            self._filename = 'WC_2015_MO_STATS_FOX'
        elif type == self.WC_2015_WO_STATS_FOX:
            self._filename = 'WC_2015_WO_STATS_FOX'
        elif type == self.WC_2015_MXO_STATS_FOX:
            self._filename = 'WC_2015_MXO_STATS_FOX'

        self._filename = csvdata.CSV_FILES + self._filename

    def write_csv_games(self, rows):
        with open(self._filename, 'w') as csv_file:
            spamwriter = csv.writer(csv_file,
                                    delimiter=';',
                                    quotechar='|',
                                    quoting=csv.QUOTE_MINIMAL
                                    )
            logging.debug('Writing CSV file: %s' % (self._filename))
            for row in self.rows:
                spamwriter.writerow(row)
            logging.debug('Done writing CSV file: %s' % (self._filename))


remote_file = WC2015_MX_URL
# local_file = WC2015_WO_FILE
local_file = WC2015_MX_FILE
# csv_name = WC2015_WO_FILE
csv_name = WC2015_MX_FILE
# generated_file = WC2015_WO_GENERATED_FILE
generated_file = WC2015_MX_GENERATED_FILE
# category = 'WO'
category = 'MX'

## download_file(remote_file, local_file)
# f = open(local_file, 'r')
# soup = BeautifulSoup(f)
# web_games = extract_games_fit(soup)
# groups = extract_groups_fit(soup)
# comp_games = assign_games_to_groups(web_games, groups)
# csv_games = games_to_csv_array(comp_games, 'World Cup 2015', category)
# write_csv(csv_games, generated_file)


## main program ###
#fox_manager = FoxGamesManager(FoxGamesManager.WC_2015_WO_FOX)
#fox_manager.extract_raw_games()
#fox_manager.extract_statistics()
# fox_manager.convert_fox_games_to_csv_games()
# for g in fox_manager.get_csv_games():
#    print(g)
# fox_manager.convert_fox_games_to_csv_games()
# for stat in fox_manager.get_csv_statistics():
#    print(stat)



# mo_writer = CsvWriter('WC', 'MO', 2015)
# wo_writer = CsvWriter('WC', 'WO', 2015)
# mxo_writer = CsvWriter('WC', 'MXO', 2015)

# mo_writer.download_raw_file()
# mo_writer.create_csv_file()

# wo_writer.download_raw_file()
# wo_writer.create_csv_file()

# mxo_writer.download_raw_file()
# mxo_writer.create_csv_file()
