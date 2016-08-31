import csv
import logging
import os.path
import re
import time

import requests
from bs4 import BeautifulSoup
from nameparser import HumanName
from player import csvdata
from player.models import GameRound
from player.models import get_player_gender

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
# Get an instance of a logger
logger = logging.getLogger(__name__)


class FitGamesManager:

    def __init__(self, tournament):
        self.tournament = tournament
        self.csv_stats = []
        self.fit_games = []
        self.t_name = csvdata.get_tournament_name(tournament)
        self.t_division = csvdata.get_tournament_division(tournament)
        self.url = csvdata.get_tournament_url(tournament)[0]
        self.raw = csvdata.get_tournament_html_path(tournament)[0]
        self.games_stats_links = list()

    def download_games_html(self, force=False):
        _download_file(self.url, self.raw)

    @staticmethod
    def download_stats_html():
        for competition, values1 in csvdata.remote_fit_stats_files.items():
            for division, values2 in values1.items():
                for team, url in values2.items():
                    _download_file(url, csvdata.local_fit_stats_files.get(competition).get(division).get(team))

    def get_csv_stats_euros_2016(self, download=False):
        url1 = "https://www.internationaltouch.org/"
        for game, url2 in zip(self.fit_games, self.games_stats_links):
            if url2:
                dst = self.get_game_statistic_file_to_save(game)
                if download:
                    _download_file(url1 + url2, dst)
                self._extract_fit_game_statistics(dst, game)
        return self.csv_stats

    def games_to_csv_array(self, games):
        result = []
        for game in games:
            g1 = csvdata.FitGame(game)
            g = csvdata.CsvGame(None, g1, self.t_name, self.t_division)
            result.append(g)
        return result

    def save_stats_info(self, games):
        for game in games:
            if not game[9]:
                self.games_stats_links.append(None)
            else:
                self.games_stats_links.append(game[9])

    def get_fit_games(self):
        with open(self.raw, 'r') as f:
            soup = BeautifulSoup(f, "lxml")
            raw_games = self._extract_fit_games(soup)
            raw_groups = self._extract_fit_pools(soup)
            raw_sorted_games = self._assign_fit_games_to_fit_pools(raw_games, raw_groups)
            self.save_stats_info(raw_sorted_games)
            self.fit_games = self.games_to_csv_array(raw_sorted_games)
            return self.fit_games

    def get_csv_stats(self):
        if not self.csv_stats:
            self._extract_fit_statistics()
        return self.csv_stats

    def _extract_fit_games(self, soup):
        games = []
        for row1 in soup.findAll('table', {"class": "round-table"}):
            game_date = row1.previous_sibling.previous_sibling.string
            for row2 in row1.findAll('tr'):
                game = list(range(8))
                if row2.find('strong', {"class": "round"}):
                    current_round = row2.find('strong', {"class": "round"}).contents[0].strip()
                if current_round in ['Semi Final 1', 'Semi Final 2']:
                    current_round = 'Semifinal'
                game[0] = current_round
                game_time = row2.find('td', {"class": "time"}).find('span').contents[0]
                game[1] = self._convert_fit_time(game_time, game_date)
                # game[1] = datetime(*game[1][:6]).isoformat()
                game[2] = row2.find('td', {"class": "field"}).find('span').contents[0]
                game[3] = row2.find('td', {"class": "home"}).find('span').contents[0]
                i = 4
                for score in row2.findAll('td', {"class": "score"}):
                    game[i] = score.contents[0]
                    i += 1
                    game[6] = row2.find('td', {"class": "away"}).find('span').contents[0]
                stats_link = row2.find('a', {"title": "Match Statistics"})
                if stats_link:
                    game[7] = stats_link.get('href')
                games.append(game)
        return games

    def _convert_fit_time(self, arg1, arg2):
        if "a.m" in arg1:
            ntime = arg1.replace("a.m.", "AM")
        elif "p.m." in arg1:
            ntime = arg1.replace("p.m.", "PM")
        ndate = re.sub('\d+', self._convert_fit_time_aux, arg2, 1)
        final_date = ndate + ' ' + ntime
        result = time.strptime(final_date, '%d %b %Y %I:%M %p')
        return result

    def _convert_fit_time_aux(self, n):
        if int(n.group(0)) < 10:
            result = str(n.group(0)).zfill(2)
        else:
            result = str(n.group(0))
        return result

    def _extract_fit_pools(self, soup):
        """
         Returns a dictionary containing as a key the pool name and as a value all the teams that belongs to such
         pool.
        :param soup: a beautiful object (parsed html)
        :return: a dictionary with the pool name as a key and all the teams that belong to such pool as a value
        """
        pools = dict()
        for row0 in soup.findAll('table', {"class": "info-table"}):
            pool = []
            for row1 in row0.tbody.findAll(['tr', 'td']):
                if row1.find('th', text=re.compile(csvdata.WC2015_RE_GROUPS)):
                    pool_name = row1.find('th', text=re.compile(csvdata.WC2015_RE_GROUPS)).get_text()
                    if len(pool_name) < 4 and pool_name != 'Cup':  # e.g.: P is a match but not valid!!
                        pool_name = GameRound.LIGA
                    elif pool_name in ['Cup Pool', 'Cup']:
                        pool_name = 'Division 1'
                    elif pool_name in ['Seeding Pool', 'Bowl']:
                        pool_name = 'Division 2'
                for row2 in row1.findAll('td', {"class": "team"}):
                    for row3 in row2.find('span').contents:
                        pool.append(row3)
                        pools[pool_name] = pool
        return pools

    def _extract_fit_pool_size(self, key, groups):
        return len(groups.get(key))

    def _assign_fit_games_to_fit_pools(self, games, groups):
        multiple_choice_list = []
        for game in games:
            local = game[3]
            visitor = game[6]
            if re.match(csvdata.WC2015_RE_FINALS, game[0]) or re.match(csvdata.EUROS2014_RE_FINALS, game[0]):
                assigned_group = 'finals'
                nteams = 2
            else:
                possible_groups = self._find_fit_game_in_fit_groups(local, visitor, groups)
                if len(possible_groups) > 1:
                    if ([local, visitor] not in multiple_choice_list) or ([visitor, local] not in multiple_choice_list):
                        assigned_group = self._find_pool_position(possible_groups, 1)
                        multiple_choice_list.append([local, visitor])
                        multiple_choice_list.append([visitor, local])
                    else:
                        assigned_group = self._find_pool_position(possible_groups, 2)
                else:
                    assigned_group = possible_groups[0]
                nteams = self._extract_fit_pool_size(assigned_group, groups)
            game.insert(0, assigned_group)
            game.insert(1, nteams)
        return games

    def _find_fit_game_in_fit_groups(self, local, visitor, groups):
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

    def _find_pool_position(self, groups, position):
        if position == 1:
            if re.match('Pool [A|B|C|D|E|F]', groups[0]):
                result = groups[0]
            elif re.match('Pool [A|B|C|D|E|F]', groups[1]):
                result = groups[1]
            elif re.match('Liga', groups[0]):
                result = groups[0]
            elif re.match('Liga', groups[1]):
                result = groups[1]
            else:
                raise ValueError('Illegal argument:', groups)

        elif position == 2:
            if re.match('Division [1|2|3]', groups[0]):
                result = groups[0]
            elif re.match('Division [1|2|3]', groups[1]):
                result = groups[1]
            else:
                raise ValueError('Illegal argument:', groups)
        else:
            raise ValueError('Illegal arguments:', groups, position)

        return result

    def _extract_fit_statistics(self):
        if os.path.exists(csvdata.RAW_STATS_FILES) and os.path.isdir(csvdata.RAW_STATS_FILES):
            self.csv_stats = []
            local_files = csvdata.get_fit_local_stats_files(self.tournament)
            for team, file_path in local_files.items():
                        with open(file_path, 'r') as f:
                            soup = BeautifulSoup(f)
                        self._extract_fit_statistic_single(soup, team)

    def _extract_fit_game_statistics(self, file_path, game):
        if os.path.exists(file_path):
            with open(file_path) as f:
                soup = BeautifulSoup(f)

                tables = soup.findAll('table')
                local = True
                team_names = list()
                h3 = soup.findAll('h3')
                for t in h3:
                    if t.get('class'):
                        team_names.append(t.text)

                for table in tables:
                    table_rows = table.find_all('tr')
                    for row in table_rows[1:]:
                        columns = row.findAll('td')
                        csv_stat = list(range(16))
                        csv_stat[0] = game.tournament_name
                        csv_stat[1] = game.division
                        if local:
                            csv_stat[2] = game.local
                        else:
                            csv_stat[2] = game.visitor
                        csv_stat[3] = columns[0].text  # number
                        full_name = columns[1].text
                        name = extract_human_name(full_name)
                        csv_stat[4] = name[0]  # first name
                        csv_stat[5] = name[1]  # last name
                        csv_stat[6] = get_player_gender(self.t_division)  # gender
                        csv_stat[7] = columns[3].text.replace('-', '0')  # scores
                        csv_stat[8] = columns[2].text.replace('-', '0')  # mvp
                        csv_stat[9] = game.local
                        csv_stat[10] = game.local_score
                        csv_stat[11] = game.visitor_score
                        csv_stat[12] = game.visitor
                        csv_stat[13] = game.category
                        csv_stat[14] = game.round
                        csv_stat[15] = game.nteams
                        self.csv_stats.append(csv_stat)
                    local = False

    def _extract_fit_statistic_single(self, soup, team):
        table_rows = soup.find(id="players").find_all('tr')
        for row in table_rows[1:]:
            csv_stat = list(range(10))
            csv_stat[0] = self.t_name
            csv_stat[1] = self.t_division
            csv_stat[2] = team.title()
            columns = row.findAll('td')
            csv_stat[3] = columns[1].contents[0]  # number
            full_name = columns[0].contents[0]
            name = extract_human_name(full_name)
            csv_stat[4] = name[0]  # first name
            csv_stat[5] = name[1]  # last name
            csv_stat[6] = get_player_gender(self.t_division)  # gender
            csv_stat[7] = columns[2].contents[0].replace('-', '0')  # played
            csv_stat[8] = columns[3].contents[0].replace('-', '0')  # scores
            csv_stat[9] = columns[4].contents[0].replace('-', '0')  # mvp
            self.csv_stats.append(csv_stat)

    def get_game_statistic_file_to_save(self, game):
        tup = (self.t_name, self.t_division, game.category, game.round, game.local, game.visitor, 'stats')
        destination = '_'.join(tup) + '.html'
        destination = destination.replace(' ', '_')
        return csvdata.RAW_STATS_FILES_EUROS + destination


class FoxGamesManager:

    phases = ['Championship', 'Plate', 'Division One Finals', 'Division Two Finals (Plate)',
              'Division Three Finals (Bowl)', 'PLAYOFF GAMES']

    def __init__(self, tournament):
        self.tournament = tournament
        self._games = []
        self._fox_games = []
        self._csv_stats = []
        self._root_website = 'http://www.foxsportspulse.com/'
        self._remote_files = csvdata.get_tournament_url(tournament)
        self._local_files = csvdata.get_tournament_html_path(tournament)
        self._tournament_name = csvdata.get_tournament_name(tournament)
        self._year = csvdata.get_tournament_year(tournament)
        self._tournament_division = csvdata.get_tournament_division(tournament)

    def download_games_html(self):
        _download_files(self._remote_files, self._local_files)

    def download_statistics_html(self):
        if len(self._fox_games) > 0:
            for game in self._fox_games:
                destination = game.get_game_statistic_file_to_save()
                _download_file(self._root_website + game.link, destination)

    def get_fox_games(self):
        if not self._fox_games:
            return self._extract_fox_games()
        else:
            return self._fox_games

    def get_csv_statistics(self):
        if not self._csv_stats:
            return self._extract_fox_statistics()
        else:
            return self._csv_stats

    def _extract_fox_games(self):
        self._fox_games = []
        for i in range(0, len(self._local_files)):
            f = open(self._local_files[i], 'r')
            soup = BeautifulSoup(f)
            self._fox_games.extend(self._extract_fox_games_single(soup))

    def _extract_fox_games_single(self, soup):
        result = []

        phase = soup.find(class_="compoptions comppage comppools").find(class_="fixoptions").find(
                class_="buttons active").contents[0]

        if phase in self.phases:
            round = 'UNKNOWN'
            category = 'Gold'
        elif 'Pool' in phase:
            round = phase
            category = 'Gold'
        elif phase == 'Division One':
            round = 'Division'
            category = 'Gold'
        elif phase == 'Division Two':
            round = 'Division'
            category = 'Silver'
        elif phase == 'Division Three':
            round = 'Division'
            category = 'Bronze'
        elif phase == 'Playoff Games':
            round = 'UNKNOWN'
            category = 'Gold'
        elif phase == 'Normal Season':
            round = 'Pool A'
            category = 'Gold'
        elif phase == 'Finals':
            round = 'UNKNOWN'
            category = 'Gold'
        else:
            print('Problem with the phase = %s' % phase)
            raise Exception('The phase is not supported')

        team_names = {}
        for row1 in soup.findAll(class_="all-fixture-wrap stacked-wide"):
            if round == 'UNKNOWN':
                try:
                    round = row1.find(class_="match-name").contents[0]
                except AttributeError:
                    round = row1.find(id="round-wrap").find(id="current-round").contents[0]
            else:
                try:
                    check = row1.find(id="round-wrap").find(id="current-round").contents[0]
                    if 'Round' not in check:
                        round = check
                except AttributeError:
                    pass
            for row2 in row1.findAll(class_="match-wrap sport-5 fixturerow "):
                n_teams = None
                if row2.find(class_="match-name"):
                    round = row2.find(class_="match-name").contents[0]
                    n_teams = 2
                if round in ['Semi Final 1', 'Semi Final 2', 'Semi Finals']:
                    round = 'Semifinal'
                    n_teams = 2
                elif round == 'Elimination Playoff One':
                    if self._tournament_division == 'M30':
                        round = GameRound.EIGHTH
                    elif self._tournament_division == 'W27':
                        round = csvdata.FIFTH_POSITION
                elif round in ['Qualifying Final One',
                               'Qualifying Final Two'] and self._tournament_division in ['M30', 'SMX']:
                    round = GameRound.QUARTER

                link = row2.find(class_="match-centre-link").find("a", href=True)
                local_team = row2.find(class_="home-team-name").find("a").contents[0]
                local_score = row2.find(class_="home-team-score").contents[0]
                visitor_team = row2.find(class_="away-team-name").find("a").contents[0]
                visitor_score = row2.find(class_="away-team-score").contents[0]
                time_date = row2.find(class_="match-time").contents[0]
                time_st = _convert_fox_time(time_date, self._year)
                field = row2.find(class_="match-venue").find("a").contents[0]
                team_names[local_team] = None
                team_names[visitor_team] = None

                date = time.strftime("%m/%d/%y", time_st)
                t = time.strftime("%H:%M", time_st)

                fgame = csvdata.FoxGame(self._tournament_name, self._tournament_division, date, t, field, round,
                                        category, n_teams, local_team, local_score, visitor_score, visitor_team,
                                        link['href'])

                result.append(fgame)

        n_teams = len(team_names)
        for game in result:
            if game.nteams is None:
                if game.round == 'Semifinal' or game.round == 'Grand Final' or game.round == 'Final':
                    game.nteams = 2
                else:
                    game.nteams = n_teams

        return result

    def _extract_fox_statistics(self):
        if os.path.exists(csvdata.RAW_STATS_FILES) and os.path.isdir(csvdata.RAW_STATS_FILES):
            self._csv_stats = []
            for filename in os.listdir(csvdata.RAW_STATS_FILES):
                string = self._tournament_name + '-' + self._tournament_division + '-'
                string = string.replace(' ', '_')
                if filename.startswith(string) and filename.endswith('.html'):
                    f = open(csvdata.RAW_STATS_FILES + filename, 'r')
                    soup = BeautifulSoup(f)
                    self._extract_fox_statistic_single(soup, filename)
        else:
            print('The directory %s does not exists.' % csvdata.RAW_STATS_FILES)
            logger.debug('The directory %s does not exists.', csvdata.RAW_STATS_FILES)

    def _extract_fox_statistic_single(self, soup, filename):
        # ['World_Cup_2015', 'WO', '05_02_15', '12_00', 'Division', 'Gold', '7', 'Singapore', '1', '1', 'Papua_New_Guinea.html']
        print('Extrating game statistic from file: %s' % filename)
        filename_parts = filename.split('-')
        if filename_parts[4] == '1_4':
            round = GameRound.QUARTER
        # elif filename_parts[4] == 'Semi Finals':
        #    round = GameRound.SEMI
        else:
            round = filename_parts[4].replace('_', ' ')
        category = filename_parts[5].replace('_', '/')
        team_numbers = filename_parts[6]
        player_gender = get_player_gender(self._tournament_division)

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
            try:
                number = tds[0].contents[0]
                int(number)
            except (IndexError, ValueError):
                number = None
            try:
                names = extract_human_name(tds[1].find(class_="playerdetail resultlink").contents[0])
            except AttributeError:
                print('###############################################################################################')
                print(tds)
                print(tds[1])
                print(tds[1].find(class_="playerdetail resultlink"))
                print('###############################################################################################')
                continue
            first_name = names[0]
            last_name = names[1]
            tries = tds[2].contents[0]
            statistic = csvdata.CsvNTSStatistic(
                    None, self._tournament_name, self._tournament_division, local, number, first_name, last_name,
                    player_gender, tries, local, local_score, visitor_score, visitor, category, round, team_numbers)
            self._csv_stats.append(statistic)

        # print(visitor_stats.find("table", {"class": "tableClass stats"}).findAll('tr')[1:])
        for tr in visitor_stats.find("table", {"class": "tableClass stats"}).findAll('tr')[1:]:
            tds = tr.findAll('td')
            try:
                number = tds[0].contents[0]
                int(number)
            except (IndexError, ValueError):
                number = None
            names = extract_human_name(tds[1].find(class_="playerdetail resultlink").contents[0])
            first_name = names[0]
            last_name = names[1]
            tries = tds[2].contents[0]
            statistic = csvdata.CsvNTSStatistic(
                    None, self._tournament_name, self._tournament_division, visitor, number, first_name, last_name,
                    player_gender, tries, local, local_score, visitor_score, visitor, category, round, team_numbers)
            self._csv_stats.append(statistic)


class CsvWriter:

    def __init__(self, tournament, is_stats=False, is_test=True):
        self._filename = csvdata.get_csv_path(tournament, is_stats, is_test)

    def write_csv(self, rows):
        with open(self._filename, 'w') as csv_file:
            spam_writer = csv.writer(csv_file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            logging.debug('Writing CSV file: %s' % self._filename)
            for row in rows:
                if isinstance(row, csvdata.CsvGame) or isinstance(row, csvdata.CsvNTSStatistic):
                    spam_writer.writerow(row.to_csv_array())
                elif isinstance(row, list):
                    spam_writer.writerow(row)
                else:
                    raise Exception('Operation not supported.')
            logging.debug('Done writing CSV file: %s' % self._filename)
        csv_file.close()

    def get_filename_path(self):
        return self._filename

    def delete_filename_path(self):
        if os.path.isfile(self._filename):
            os.remove(self._filename)


def extract_human_name(name):
    result = list(range(2))
    human_name = HumanName(name)

    if human_name.middle:
        result[0] = human_name.first + " " + human_name.middle
    else:
        result[0] = human_name.first
    result[1] = human_name.last

    return result


def _download_files(src_list, dst_list):
    if len(src_list) != dst_list:
        raise ValueError("List arguments have different length.")
    for i in range(0, len(src_list)):
        _download_file(src_list[i], dst_list[i])


def _download_file(src, dst):
    logger.debug('Downloading remote file: %s\nTo local file %s', src, dst)
    page = requests.get(src)
    with open(dst, 'wb') as code:
        code.write(page.content)
    logger.debug('Download complete')


def _convert_fox_time(arg, year):
    arg = arg.replace(u'\xa0', ' ')
    aux = arg.split(' / ', maxsplit=1)
    result = time.strptime(aux[0] + " " + aux[1] + " " + str(year), "%I:%M %p %a %d %b %Y")
    return result
