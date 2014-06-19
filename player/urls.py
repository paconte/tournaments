from django.conf.urls import patterns, url

from player import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<tournament_id>\d+)/$', views.detail_tournament, name='detail_tournament'),
    url(r'^(?P<tournament_id>\d+)/team/(?P<team_id>\d+)/$', views.detail_team, name='detail_team'),
#    url(r'^/player/(?P<player_id>\d+)/$', views.detail_player, name='detail_player'),
)
