from django.conf.urls import patterns, url

from player import views
#from player.views import GameView
from player.gameView import GameView, TeamView, TournamentView

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
#    url(r'^(?P<tournament_id>\d+)/$', views.detail_tournament, name='detail_tournament'),
#    url(r'^(?P<tournament_id>\d+)/team/(?P<team_id>\d+)/$', views.detail_team, name='detail_team'),
#    url(r'^(?P<tournament_id>\d+)/game/(?P<game_id>\d+)/$', views.detail_game, name='detail_game'),
#    url(r'^/player/(?P<player_id>\d+)/$', views.detail_player, name='detail_player'),
    url(r'^game/(?P<pk>\d+)/$', GameView.as_view(), name='detail_game'),
    url(r'^(?P<tournament_id>\d+)/team/(?P<pk>\d+)/$', TeamView.as_view(), name='detail_team'),
    url(r'^(?P<pk>\d+)/$', TournamentView.as_view(), name='detail_tournament'),
)
