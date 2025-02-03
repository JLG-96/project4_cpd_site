from django.contrib import admin
from .models import Team, Fixture

# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'home_ground', 'founded_year', 'games_played', 'wins', 'draws', 'losses', 'goals_for', 'goals_against', 'points', 'logo')
    search_fields = ['name', 'manager']

class FixtureAdmin(admin.ModelAdmin):
    list_display = ('opponent', 'date', 'time', 'home_or_away', 'location', 'goals_for', 'goals_against', 'match_completed')
    list_filter = ('date', 'home_or_away', 'match_completed')  # Allows filtering by date, home/away, and match status
    search_fields = ['opponent', 'location']


admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)
