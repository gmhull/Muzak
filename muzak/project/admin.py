from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from leagues.admin import PlayerInline
from .models import MuzakUser
from nested_inline.admin import NestedModelAdmin

# Register your models here.
class MuzakUserAdmin(BaseUserAdmin):
    inlines = (PlayerInline,)


admin.site.register(MuzakUser, MuzakUserAdmin)
