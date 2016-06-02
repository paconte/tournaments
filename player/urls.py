from django.conf.urls import patterns, url

from player import views
from player.classViews import GameView
from player.classViews import PersonView
from player.classViews import TeamView
from player.classViews import TeamTournamentView
from player.classViews import TournamentView


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^add_tournament', views.add_tournament, name='add_tournament'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^search', views.search, name='search'),
    url(r'^game/(?P<pk>\d+)/$', GameView.as_view(), name='detail_game'),
    url(r'^team/(?P<pk>\d+)/$', TeamView.as_view(), name='detail_team'),
    url(r'^person/(?P<pk>\d+)/$', PersonView.as_view(), name='detail_person'),
    url(r'^(?P<tournament_id>\d+)/team/(?P<pk>\d+)/$', TeamTournamentView.as_view(), name='detail_team_tournament'),
    url(r'^(?P<pk>\d+)/$', TournamentView.as_view(), name='detail_tournament'),
)
