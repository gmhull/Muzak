from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from leagues.admin import PlayerInline
from .models import MuzakUser

# Register your models here.
class MuzakUserAdmin(admin.ModelAdmin):
    # list_display = ('profile_img',)
    inlines = (PlayerInline,)


admin.site.register(MuzakUser, MuzakUserAdmin)
