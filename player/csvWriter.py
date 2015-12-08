from bs4 import BeautifulSoup
from lxml import html
import copy
import csv
import csvdata
import logging
import os.path
import re
import requests
import time

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


class CsvWriter:
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


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
a = CsvWriter('WC', 'MO', 2015)
#a.download_raw_file()
a.create_csv_file()
