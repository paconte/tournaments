from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
from django.shortcuts import get_object_or_404

from player.models import Tournament
from player.models import Game
from player.models import GameRound
from player.models import Team
from player.models import Player
from player.models import PlayerStadistic

from django.views.generic import DetailView
from player.forms import ContactForm

from service import *

# Create your views here.

def index(request):
    """
    Prepare and displays the main view of the web application.

    Args:
        request: django HttpRequest class
    Returns:
        A django HttpResponse class
    """
    tournament_list = Tournament.objects.all()
    template = loader.get_template('tournaments/index.html')
    context  = RequestContext(request, {'tournament_list': tournament_list, })
    return HttpResponse(template.render(context))

def about(request):
    """
    Prepare and displays the about view of the web application.

    Args:
        request: django HttpRequest class
    Returns:
        A django HttpResponse class
    """

    tournament_list = Tournament.objects.all()
    template = loader.get_template('tournaments/about.html')
    context  = RequestContext(request, {'tournament_list': tournament_list, })
    return HttpResponse(template.render(context))

def contact(request):
    """
    Displays the contact view of the web application.

    Args:
        request: django HttpRequest class
    Returns:
        A django HttpResponse class. This view displays a form, in case the form is successfully 
        fulfilled and sent, the same view is displayed with a success message and an empty form. 
        Otherwise the form will be again rendered with error messages.
    """

    success = False          # true iff form has been saved otherwise false
    tournament_list = Tournament.objects.all()
    template = loader.get_template('tournaments/contact.html')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            success = True
            contactEntry = form.save()
            form = ContactForm()
    else:
        form = ContactForm()

    context  = RequestContext(request, {'tournament_list': tournament_list,
                                        'form': form,
                                        'sucess': success })
        
    return HttpResponse(template.render(context))

def detail_tournament(request, tournament_id):
    """
    Prepare and displays a tournament view of a user selected tournament.

    Args:
        request: django HttpRequest class
        tournament_id: the id of the tournament selected by the user
    Returns:
        A django HttpResponse class
    """

    # Database requests
    tournament_list = Tournament.objects.all()
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    games = Game.objects.filter(tournament=tournament_id)
    teams = Team.objects.filter(tournament__id=tournament_id)

    # Data to save the different tournament games
    liga_games = [] 
    pool_games = []
    playoffs_games = []

    # Divide the different tournament games by phases
    for game in games:
        if game.phase.round == GameRound.LIGA:
            liga_games.append(game)
        elif (game.phase.round == GameRound.POOL_A 
              or game.phase.round == GameRound.POOL_B        
              or game.phase.round == GameRound.POOL_C
              or game.phase.round == GameRound.POOL_D):
            pool_games.append(game)        
        else:
            playoffs_games.append(game)

    # Apply algorithms to the games and store it in different data structures. When rendering the
    # view we need the data to be sorted and classified properly because the html code expect it so.
    fixtures = Fixtures(games)
    fixtures.sort_pools()
    teams_matrix = TeamsMatrix(3, teams)
    st_utils = StructuresUtils()

    return render(request, 
                  'tournaments/detail_tournament.html', 
                  {'tournament_list': tournament_list, 
                   'tournament': tournament,                             # tournament info
                   'games': games,                                       # all tournament games
                   'sorted_pools': fixtures.sorted_pools,                # sorted pool games
                   'finals':fixtures.get_finals({}),                     # sorted playoff/finals games
                   'teams_matrix': st_utils.get_teams_matrix(teams, 4),})# tournament teams

def detail_team(request, tournament_id, team_id):    
    """
    Prepare and displays a team view for a specific tournament.

    Args:
        request: django HttpRequest class
        tournament_id: the id of the tournament selected by the user
        team_id: the id of the team selected by the user
    Returns:
        A django HttpResponse class. Render a team view web site. This team view is specific for a
        given tournament.
    """

    # Database requests
    tournament_list = Tournament.objects.all()
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    team = get_object_or_404(Team, pk=team_id)
    games = Game.objects.filter(Q(tournament=tournament_id), Q(local=team_id) | Q(visitor=team_id))    
    players = Player.objects.filter(team=team_id)
    stadistics = []
    for player in players:
        stadistics.extend(PlayerStadistic.objects.filter(player=player.id))
    st_utils = StructuresUtils()

    return render(request, 'tournaments/detail_team.html', 
                  {'team': team, 
                   'games': st_utils.get_team_view_games(games), 
                   'players': st_utils.get_team_details_matrix(stadistics, players), 
                   'tournament_list': tournament_list,
                   'tournament': tournament, })

"""
def detail_team_all(request, team_id):
    games = Game.objects.filter(Q(local=team_id) | Q(visitor=team_id))    
    players = Player.objects.filter(team=team_id)
    stadistics = []
    for player in players:
        stadistics.extend(PlayerStadistic.objects.filter(player=player.id))
    
    return render(request, 'tournaments/detaul_team_all.html',
                  {'team': team, 'games': games, 'players': players})        
"""
def detail_game(request, game_id):
    """
    Prepare and displays a game view.

    Args:
        request: django HttpRequest class
        game_id: the id of the game selected by the user
    Returns:
        A django HttpResponse class
    """

    # Database requests
    tournament_list = Tournament.objects.all()
    game = Game.objects.filter(pk=game_id)
    stadistics = PlayerStadistic.objects.filter(game=game_id)
    local_players = Player.objects.filter(team=game[0].local)
    visitor_players = Player.objects.filter(team=game[0].visitor)

    # Apply algorithms to the games and store it in different data structures. When rendering the
    # view we need the data to be sorted and classified properly because the html code expect it so.
    st_utils = StructuresUtils()
    st_utils.get_game_details_matrix(stadistics, local_players, visitor_players)

    return render(request, 'tournaments/detail_game.html',
                  {'game': game[0],
                   'stadistics': st_utils.get_game_details_matrix(stadistics,
                                                                  local_players,
                                                                  visitor_players),
                   'tournament_list': tournament_list, })
