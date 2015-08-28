import csv
import os.path

from player.models import Tournament
from player.models import Team
from player.models import Person
from player.models import Player
from player.models import Game
from player.models import GameRound
from player.models import PlayerStadistic



# PLAYER_STADISTICS_INDEXES
PL_ST_TORNAMENT_INDEX = 0
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


def create_or_fetch_person(row):
    try:
        result = Person.objects.get(
            first_name = row[PL_ST_FIRST_NAME_INDEX],
            last_name = row[PL_ST_LAST_NAME_INDEX]
        )
    except Person.objects.MultipleObjects:
        if (row[PL_ST_GENDER_INDEX]):
            result = Person.objects.get(
                first_name = row[PL_ST_FIRST_NAME_INDEX],
                last_name = row[PL_ST_LAST_NAME_INDEX],
                gender = row[PL_ST_GENDER_INDEX],
            )
    except Person.objects.ObjectDoesNotExist:        
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

def create_or_fetch_player_stadistic(pGame, pPlayer, row):
    result = None
    if (row[PL_ST_PLAYER_TRIES_INDEX] and int(row[PL_ST_PLAYER_TRIES_INDEX]) > 0):
        result = PlayerStadistic.objects.get_or_create(
            game = pGame,
            player = pPlayer,
            points = row[PL_ST_PLAYER_TRIES_INDEX]
        )
    return result
    
def fetch_game(pTournament, pLocal, pVisitor, row):    
    get_round = row[PL_ST_GAME_ROUND_INDEX]
    if (get_round == '\xc2\xbc'):
        get_round = '1/4'
    get_game_phase = GameRound.objects.get(
        category = row[PL_ST_GAME_CATEGORY_INDEX],
        round = get_round,
        number_teams = row[PL_ST_PHASE_TEAMS_INDEX]                                    
    )
    print 'Found phase:\n %s' %(get_game_phase)

    try:
        #first try with given local and visitor teams and scores:
        get_game = Game.objects.get(
            tournament = pTournament.id,
            local = pLocal.id,
            visitor = pVisitor.id,
            local_score = row[PL_ST_LOCAL_TEAM_SCORE_INDEX],
            visitor_score = row[PL_ST_VISITOR_TEAM_SCORE_INDEX],
            phase = get_game_phase.id            
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
            phase = get_game_phase
    )
    return get_game

def printCF(obj, created):
    if (obj):
        if (created):
            print 'Created %s:\n %s' %(obj.__class__.__name__, obj)
        else:
            print 'Found %s:\n %s' %(obj.__class__.__name__, obj)
    else:
        print 'Skip PlayerStadistic\n'

def readTournamentStadisticRow(row):    
    get_tournament = Tournament.objects.get(
        name = row[PL_ST_TORNAMENT_INDEX],
        division = row[PL_ST_DIVISION_INDEX]
    )
    printCF(get_tournament, False)
    
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

        get_game = fetch_game(get_tournament, get_local_team, get_visitor_team, row)
        printCF(get_game, False)
        
        get_player_stadistic, created = create_or_fetch_player_stadistic(
            get_game,
            get_player,
            row
        )
        printCF(get_player_stadistic, created)
    else:
        print 'GameStadistic skipped: there is no scores for player: %s\n ' % (get_player)    
    
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
    
fname = './player/test.csv'
if os.path.isfile(fname):
    readTournamentStadistic(fname)
else:
    print 'ERROR: %s is not a file' % (fname)

