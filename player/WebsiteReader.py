from lxml import html
import requests
import re
import time
import csv
import copy

from datetime import datetime
from bs4 import BeautifulSoup

#CONSTANTS
WC2015_MO_GENERATED_FILE = './WC2015_MO_GENERATED.csv'
WC2015_WO_GENERATED_FILE = './WC2015_WO_GENERATED.csv'
WC2015_MX_GENERATED_FILE = './WC2015_MX_GENERATED.csv'
WC2015_MO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mens/'
WC2015_WO_URL = 'http://www.internationaltouch.org/events/world-cup/2015/womens/'
WC2015_MX_URL = 'http://www.internationaltouch.org/events/world-cup/2015/mixed/'
WC2015_MO_FILE = './WC2015_MO.txt'
WC2015_WO_FILE = './WC2015_WO.txt'
WC2015_MX_FILE = './WC2015_MX.txt'
WC2015_RE_GROUPS = '[Pool [A|B|C|D|E|F]|Division [1|2|3]'
WC2015_RE_FINALS = '[Grand Final|Bronze|Playoff ]'
FINALS_CONVERSION_DICT = {'Grand Final':'Final',
                          'Bronze':'Third position',
                          'Playoff 5th/6th':'Fifth position',
                          'Playoff 7th/8th':'Seventh position',
                          'Playoff 9th/10th':'Ninth position',
                          'Playoff 11th/12th':'Eleventh position',
                          'Playoff 13th/14th':'Thirteenth position',
                          'Playoff 15th/16th':'Fifteenths position'}

def downloadFile(src, dst):
    page = requests.get(src)
    with open(dst, 'wb') as code:
        code.write(page.content)

def find_group_position(groups, position):
    if (position == 1):
        if (re.match('Pool [A|B|C|D|E|F]', groups[0])):
            result = groups[0]
        elif (re.match('Pool [A|B|C|D|E|F]', groups[1])):
            result = groups[1]
        else:
            raise Exception('Illegal Argument')
    elif (position == 2):
        if (re.match('Division [1|2|3]', groups[0])):
            result = groups[0]
        elif (re.match('Division [1|2|3]', groups[1])):
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

def extract_groups(soup):
    pools = dict()
    for row0 in soup.findAll('table', {"class" : "info-table"}):
        pool = []
        for row1 in row0.tbody.findAll(['tr', 'td']):
            if row1.find('th', text = re.compile(WC2015_RE_GROUPS)):
                pool_name = row1.find('th', text = re.compile(WC2015_RE_GROUPS)).get_text()
            for row2 in row1.findAll('td', {"class" : "team"}):
                for row3 in row2.find('span').contents:
                    pool.append(row3)
                    pools[pool_name] = pool
    return pools

def extract_games(soup):
    games = []
    for row1 in soup.findAll('table', {"class" : "round-table"}):
        game_date = row1.previous_sibling.previous_sibling.string
        for row2 in row1.findAll('tr'):
            game = range(7)
            if (row2.find('strong', {"class" : "round"})):
                current_round = row2.find('strong', {"class" : "round"}).contents[0].strip()
            game[0] = current_round
            game_time = row2.find('td', {"class" : "time"}).find('span').contents[0]
            game[1] = convert_time(game_time, game_date)
#            game[1] = datetime(*game[1][:6]).isoformat()
            game[2] = row2.find('td', {"class" : "field"}).find('span').contents[0]
            game[3] = row2.find('td', {"class" : "home"}).find('span').contents[0]
            i = 4            
            for score in row2.findAll('td', {"class" : "score"}):
                game[i] = score.contents[0]
                i += 1
                game[6] = row2.find('td', {"class" : "away"}).find('span').contents[0]
            games.append(game)
    return games

def rep1(n):
    if (int(n.group(0)) < 10):
        result = str(n.group(0)).zfill(2)
    else:
        result = str(n.group(0))
    return result

def convert_time(arg1, arg2):
    if "a.m" in arg1:
        ntime = arg1.replace("a.m.", "AM")
    elif "p.m." in arg1:
        ntime = arg1.replace("p.m.", "PM")
    ndate = re.sub('\d+', rep1, arg2, 1)
    final_date = ndate + ' ' + ntime
    result =  time.strptime(final_date, '%d %b %Y %I:%M %p')
    return result

def get_game_nteams(game):
    return game[1]
def get_game_date(game):
    return time.strftime("%m/%d/%y", game[3])
def get_game_time(game):
    return time.strftime("%H:%M", game[3])
def get_game_field(game):
    return game[4]
def get_game_local(game):
    return game[5]
def get_game_local_score(game):
    return game[6]
def get_game_visitor_score(game):
    return game[7]
def get_game_visitor(game):
    return game[8]

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
                                delimiter = ';',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL
        )
        for game in games:
            spamwriter.writerow(game)




#remote_file = WC2015_WO_URL
remote_file = WC2015_MX_URL
#local_file = WC2015_WO_FILE
local_file = WC2015_MX_FILE
#csv_name = WC2015_WO_FILE
csv_name = WC2015_MX_FILE
#generated_file = WC2015_WO_GENERATED_FILE
generated_file = WC2015_MX_GENERATED_FILE
#category = 'WO'
category = 'MX'

#downloadFile(remote_file, local_file)
f = open(local_file, 'r')
soup =  BeautifulSoup(f)
web_games = extract_games(soup)
groups = extract_groups(soup)
comp_games = assign_games_to_groups(web_games, groups)
csv_games = games_to_csv_array(comp_games, 'World Cup 2015', category)
write_csv(csv_games, generated_file)
for game in csv_games:
    print '%s\n' % (game)
    break
    
print 'len(web_games) = %s' % len(web_games)
print 'len(comp_games) = %s' % len(comp_games)
print 'len(csv_games) = %s' % len(csv_games)
    



