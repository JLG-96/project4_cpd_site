from django.contrib import admin
from .models import Team

# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'home_ground', 'founded_year', 'games_played', 'wins', 'draws', 'losses', 'goals_for', 'goals_against', 'points', 'logo')
    search_fields = ['name', 'manager']


admin.site.register(Team, TeamAdmin)
