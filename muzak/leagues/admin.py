from django.contrib import admin
from leagues.models import League, PlayerManager, Round, Song
from project.models import MuzakUser
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


# Register your models here.
class PlayerInline(admin.TabularInline):
    model = PlayerManager
    list_display = ('nickname', 'points',)
    extra = 0
    # readonly_fields = ('league',)

class SongInline(NestedStackedInline):
    model = Song
    extra = 1
    fk_name = 'round'
    readonly_fields = ('league',)


class RoundInline(NestedStackedInline):
    model = Round
    inlines = [SongInline,]
    extra = 1
    fk_name = 'league'


class LeagueAdmin(NestedModelAdmin):
    list_display = ('name', 'description',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RoundInline,]


admin.site.register(League, LeagueAdmin)
