from django.contrib import admin
from leagues.models import League, Player, Round, Song
from project.models import MuzakUser
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


# Register your models here.
class PlayerInline(admin.TabularInline):
    model = Player
    list_display = ('nickname', 'points',)
    extra = 1

class SongInline(NestedStackedInline):
    model = Song
    extra = 1
    fk_name = 'round'

class RoundInline(NestedStackedInline):
    model = Round
    inlines = [SongInline,]
    extra = 1
    fk_name = 'league'

class LeagueAdmin(NestedModelAdmin):
    list_display = ('name', 'description',)
    inlines = [RoundInline]


admin.site.register(League, LeagueAdmin)
