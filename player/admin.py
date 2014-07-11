from django.contrib import admin
from player.models import Person
from player.models import Team
from player.models import Player
from player.models import Game
from player.models import PlayerStadistic
from player.models import Tournament
from player.models import GameRound

# Custom admin models

class GameAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'local', 'local_score', 'visitor_score', 'visitor', 'phase')

    fieldsets = [
        ('Tournament', {'fields' : ['tournament']}),
        ('Score'     , {'fields' : ['local', 'local_score', 'visitor_score', 'visitor']}),
        ('Round'     , {'fields' : ['phase']}),
        ]


# Register your models here.
admin.site.register(Person)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Game, GameAdmin)
#admin.site.register(Game)
admin.site.register(PlayerStadistic)
admin.site.register(Tournament)
admin.site.register(GameRound)
