import csv
import os.path
import urllib2

from player.models import Tournament
from player.models import Team
from player.models import Person
from player.models import Player
from player.models import Game
from player.models import GameRound
from player.models import GameField
from player.models import PlayerStadistic

from django.db.models import TimeField

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
#TG_GAME_ROUND_INDEX = 8
TG_LOCAL_TEAM_INDEX = 9
TG_LOCAL_TEAM_SCORE_INDEX = 10
TG_VISITOR_TEAM_SCORE_INDEX = 11
TG_VISITOR_TEAM_INDEX = 12

def create_or_fetch_person(row):
    try:
        result = Person.objects.get(
            first_name = row[PL_ST_FIRST_NAME_INDEX],
            last_name = row[PL_ST_LAST_NAME_INDEX]
        )
        result = result, False
    except MultipleObjectsReturned:
        if (row[PL_ST_GENDER_INDEX]):
            result = Person.objects.get(
                first_name = row[PL_ST_FIRST_NAME_INDEX],
                last_name = row[PL_ST_LAST_NAME_INDEX],
                gender = row[PL_ST_GENDER_INDEX],
            )
            result = result, False
    except ObjectDoesNotExist:
        if (row[PL_ST_GENDER_INDEX]):
            result = Person.objects.get_or_create(
                first_name = row[PL_ST_FIRST_NAME_INDEX],
                last_name = row[PL_ST_LAST_NAME_INDEX],
                gender = row[PL_ST_GENDER_INDEX],
            )
        else:
            result = Person.objects.get_or_create(
                first_name = row[PL_ST_FIRST_NAME_INDEX],
                last_name = row[PL_ST_LAST_NAME_INDEX]
            )
    return result

def create_or_fetch_team(pName, pDivision):
    result = Team.objects.get_or_create(
        name = pName,
        division = pDivision,
    )
    return result

def add_team_to_tournament(pTournament, pTeam):
    pTournament.teams.add(pTeam)
    pTournament.save()

def create_or_fetch_player_stadistic(pGame, pPlayer, row):
    result = None
    if (row[PL_ST_PLAYER_TRIES_INDEX] and int(row[PL_ST_PLAYER_TRIES_INDEX]) > 0):
        result = PlayerStadistic.objects.get_or_create(
            game = pGame,
            player = pPlayer,
            points = row[PL_ST_PLAYER_TRIES_INDEX]
        )
    return result

def get_game_phase(pCategory, pRound, pNumber, create):
    get_round = pRound
    if (get_round == '\xc2\xbc'):
        get_round = '1/4'

    if create:
        result = GameRound.objects.get_or_create(
            category = pCategory,
            round = get_round,
            number_teams = pNumber
        )
    else:
        result = GameRound.objects.get(
            category = pCategory,
            round = get_round,
            number_teams = pNumber
        ), False
    return result

def create_game_tournament(pTournament, pLocal, pVisitor, row):
    game_phase, created = get_game_phase(row[TG_CATEGORY_INDEX],
                                         row[TG_PHASE_INDEX],
                                         row[TG_PHASE_TEAMS_INDEX],
                                         False)
    print 'Found phase:\n %s' %(game_phase)


    if row[TG_FIELD_INDEX]:
        get_field, created = GameField.objects.get_or_create(name = row[TG_FIELD_INDEX])
        printCF(get_field, created)
    else:
        get_field = None
        
    if row[TG_TIME_INDEX]:
        get_time = row[TG_TIME_INDEX]        
    else:
        get_time = None
        
    game = Game.objects.create(
        tournament = pTournament,
        local = pLocal,
        visitor = pVisitor,
        local_score = row[TG_LOCAL_TEAM_SCORE_INDEX],
        visitor_score = row[TG_VISITOR_TEAM_SCORE_INDEX],
        phase = game_phase,
        field = get_field,
        time = get_time
    )
    return game
    
    
def fetch_game_stadistic(pTournament, pLocal, pVisitor, row): 
    game_phase = get_game_phase(row[PL_ST_GAME_CATEGORY_INDEX],
                                row[PL_ST_GAME_ROUND_INDEX],
                                row[PL_ST_PHASE_TEAMS_INDEX],
                                False)
    print 'Found phase:\n %s' %(game_phase)

    try:
        #first try with given local and visitor teams and scores:
        get_game = Game.objects.get(
            tournament = pTournament.id,
            local = pLocal.id,
            visitor = pVisitor.id,
            local_score = row[PL_ST_LOCAL_TEAM_SCORE_INDEX],
            visitor_score = row[PL_ST_VISITOR_TEAM_SCORE_INDEX],
            phase = game_phase.id            
        )
        return get_game
    except Game.DoesNotExist:
        #ignore excetion and go for a second try
        pass
    #second try changing local and visitor teams and scores:
    get_game = Game.objects.get(
            tournament = pTournament,
            visitor = pLocal,
            local = pVisitor,
            visitor_score = int(row[PL_ST_LOCAL_TEAM_SCORE_INDEX]),
            local_score = int(row[PL_ST_VISITOR_TEAM_SCORE_INDEX]),
            phase = game_phase
    )
    return get_game

def get_or_create_tournament(pName, pDivision):
    result = Tournament.objects.get_or_create(name = pName, division = pDivision)
    return result
    
def printCF(obj, created):
    if (obj):
        if (created):
            print 'Created %s:\n %s' %(obj.__class__.__name__, obj)
        else:
            print 'Found %s:\n %s' %(obj.__class__.__name__, obj)
    else:
        print 'ERROR\n'

def readTournamentStadisticRow(row):
    tournament = get_or_create_tournament(row[PL_ST_TOURNAMENT_INDEX], row[PL_ST_DIVISION_INDEX])
    printCF(tournament, False)
    
    get_team = Team.objects.get(name = row[PL_ST_TEAM_INDEX])
    printCF(get_team, False)
            
    get_person, created = create_or_fetch_person(row)
    printCF(get_person, created)

    get_player, created = Player.objects.get_or_create(
        person = get_person,
        team = get_team,
        number = row[PL_ST_NUMBER_INDEX]
    )
    printCF(get_player, created)

    if row[PL_ST_VISITOR_TEAM_SCORE_INDEX]:
        get_local_team = Team.objects.get(name = row[PL_ST_LOCAL_TEAM_INDEX])
        printCF(get_local_team, False)
    
        get_visitor_team = Team.objects.get(name = row[PL_ST_VISITOR_TEAM_INDEX])
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
        print 'GameStadistic skipped: there is no scores for player: %s\n ' % (get_player)    
    
def readTournamentGameRow(row):
    tournament, created = get_or_create_tournament(row[TG_TOURNAMENT_INDEX], row[TG_DIVISION_INDEX])
    printCF(tournament, created)
    
    local_team, created = create_or_fetch_team(row[TG_LOCAL_TEAM_INDEX], row[TG_DIVISION_INDEX])
    printCF(local_team, created)

    if (created):
        add_team_to_tournament(tournament, local_team)

    visitor_team, created = create_or_fetch_team(row[TG_VISITOR_TEAM_INDEX], row[TG_DIVISION_INDEX])
    printCF(visitor_team, created)

    if (created):
        add_team_to_tournament(tournament, visitor_team)

    game = create_game_tournament(tournament, local_team, visitor_team, row)
    printCF(game, True)

def readTournamentStadistic(file):
    print '\nStarting reading tournament stadistics from %s\n' % (file)
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if any(row):
                if(row[0] == '####'):
                    print '\n Forcef exit #### :)\n'
                    break                
                print '\nRow to read:\n %s\n' %(row)
                readTournamentStadisticRow(row)
    print '\nFinished reading tournament stadistics...\n'

def readTournamentGames(file):
    print '\nStarting reading tournament games from %s\n' % (file)
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if any(row):
                if(row[0] == '####'):
                    print '\n Forcef exit #### :)\n'
                    break                
                print '\nRow to read:\n %s\n' %(row)
                readTournamentGameRow(row)
    print '\nFinished reading tournament games...\n'

def readPhases(file):
    print '\nStarting reading phases from %s\n' % (file)
    with open(file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if any(row):
                if(row[0] == '####'):
                    print '\n Forcef exit #### :)\n'
                    break                
                print '\nRow to read:\n %s\n' %(row)
                phase, created = get_game_phase(row[PH_CATEGORY_INDEX],
                                                row[PH_PHASE_ROUND_INDEX],
                                                row[PH_PHASE_TEAMS_INDEX],
                                                True)
                printCF(phase, created)
    print '\nFinished reading phases...\n'
                    

def readWC2015(fname):
    response = urllib2.urlopen(fname)
    html = response.read()
    print html

#fname = './player/test.csv'
#fname = './player/TPhases.csv'
fname = './player/WC-Games.csv'
if os.path.isfile(fname):
    if (fname == './player/WC-Games.csv'):
        readTournamentGames(fname)
    elif (fname == './player/TPhases.csv'):
        readPhases(fname)
    elif (fname == './player/test.csv'):
        readTournamentStadistic(fname):
else:
    print 'ERROR: %s is not a file' % (fname)
    
#fname = 'http://www.touchworldcup.com/'
#fname = 'http://www.foxsportspulse.com/comp_info.cgi?a=ROUND&compID=360314&c=1-9035-0-0-0'
#readWorldCup(fname)

