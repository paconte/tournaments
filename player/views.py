from django.db.models import Q
from django.http import HttpResponse
from django.template import RequestContext, loader

from player.forms import ContactForm
from player.forms import SearchForm
from player.forms import TournamentSearchForm
from player.forms import PersonSearchForm
from player.forms import TeamSearchForm
from player.models import Person
from player.models import Team
from player.models import Tournament
from player.service import sort_tournament_list

from django.conf import settings

tournament_type = settings.TOURNAMENT_TYPE


def index(request):
    """
    Prepare and displays the main view of the web application.

    Args:
        request: django HttpRequest class
    Returns:
        A django HttpResponse class
    """
    tournament_list = _get_tournament_list()
    sort_tournament = sort_tournament_list(tournament_list, tournament_type)
    template = loader.get_template('index.html')
    context = RequestContext(request, _get_tournaments_context(sort_tournament))
    return HttpResponse(template.render(context))


def about(request):
    """
    Prepare and displays the about view of the web application.

    Args:
        request: django HttpRequest class
    Returns:
        A django HttpResponse class
    """
    template = loader.get_template('about.html')
    return HttpResponse(template.render())


def add_tournament(request):
    template = loader.get_template('add_tournament.html')
    return HttpResponse(template.render())


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

    success = False  # true if form has been saved otherwise false
    template = loader.get_template('contact.html')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            success = True
            contactEntry = form.save()
            form = ContactForm()
    else:
        form = ContactForm()

    return HttpResponse(template.render())


def search(request):
    template = loader.get_template('search.html')
    success = False
    result_size = 0
    teams, persons, tournaments = [], [], []

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            if text is not None and len(text) > 0:
                teams = Team.objects.filter(name__icontains=text)
                persons = Person.objects.filter(Q(first_name__icontains=text) | Q(last_name__icontains=text))
                tournaments = Tournament.objects.filter(name__icontains=text)
                result_size = len(teams) + len(persons) + len(tournaments)
                if result_size > 0:
                    success = True
    else:
        form = SearchForm()

    context = RequestContext(request, {'form': form,
                                       'result_teams': teams,
                                       'result_tournaments': tournaments,
                                       'result_persons': persons,
                                       'result_size': result_size,
                                       'success': success
                                       })

    return HttpResponse(template.render(context))


def tournaments(request):
    tournament_list = _get_tournament_list()
    sort_tournament = sort_tournament_list(tournament_list, tournament_type)
    template = _get_tournaments_template()
    context = RequestContext(request, _get_tournaments_context(sort_tournament))
    return HttpResponse(template.render(context))


def search_team(request):
    template = loader.get_template('search_team.html')
    success = False
    teams = None

    if request.method == 'GET':
        form = TeamSearchForm(request.GET)
        if form.is_valid():
            teams = Team.objects.filter(name__icontains=form.cleaned_data.get('name'))
            if teams:
                success = True
    else:
        form = TeamSearchForm()

    context = RequestContext(request, {'form': form, 'result': teams, 'success': success})

    return HttpResponse(template.render(context))


def search_person(request):
    template = loader.get_template('search_person.html')
    success = False
    persons = None

    if request.method == 'GET':
        form = PersonSearchForm(request.GET)
        if form.is_valid():
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            if len(fname) > 0 and len(lname) > 0:
                persons = Person.objects.filter(Q(first_name__icontains=form.cleaned_data.get('first_name'))
                                                | Q(last_name__icontains=form.cleaned_data.get('last_name')))
            elif len(fname) > 0:
                persons = Person.objects.filter(first_name__icontains=form.cleaned_data.get('first_name'))
            elif len(lname) > 0:
                persons = Person.objects.filter(last_name__icontains=form.cleaned_data.get('last_name'))

            if persons:
                success = True
    else:
        form = PersonSearchForm()

    context = RequestContext(request, {'form': form, 'result': persons, 'success': success})

    return HttpResponse(template.render(context))


def search_tournament(request):
    template = loader.get_template('search_tournament.html')
    success = False
    tournaments = None

    if request.method == 'GET':
        form = TournamentSearchForm(request.GET)
        if form.is_valid():
            tournaments = Tournament.objects.filter(name__icontains=form.cleaned_data.get('name'))
            if tournaments:
                success = True
    else:
        form = TournamentSearchForm()

    context = RequestContext(request, {'form': form, 'result': tournaments, 'success': success})

    return HttpResponse(template.render(context))


# non view functions here.
def add_data_for_tournaments_menu(context):
    if tournament_type == "TOUCH":
        tournament_list = _get_tournament_list()
        sorted_tournaments = sort_tournament_list(tournament_list)
        context['australia'] = sorted_tournaments['Australia']
        context['england'] = sorted_tournaments['England']
        context['germany'] = sorted_tournaments['Germany']
        context['world_cup'] = sorted_tournaments['World_Cup']
        context['euros'] = sorted_tournaments['Euros']
        return context
    else:
        context['tournaments']


# private functions here.
def _get_tournament_list():
    return Tournament.objects.filter(type=tournament_type)


def _get_tournaments_context(sort_tournament):
    if tournament_type == "TOUCH":
        if sort_tournament:
            tournament_list = True
        else:
            tournament_list = False
        return {'tournament_list': tournament_list,
                'england': sort_tournament['England'],
                'germany': sort_tournament['Germany'],
                'world_cup': sort_tournament['World_Cup'],
                'australia': sort_tournament['Australia'],
                'euros': sort_tournament['Euros']}
    elif tournament_type == "PADEL":
        return {'tournaments': _get_tournament_list()}


def _get_tournaments_template():
    if tournament_type == "TOUCH":
        template = 'touch/tournaments.html'
    elif tournament_type == "PADEL":
        template = 'padel/tournaments.html'
    else:
        raise AttributeError('tournament type is not supported')
    return loader.get_template(template)
