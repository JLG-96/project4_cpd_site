from django.contrib import admin
from .models import Team, Fixture, Profile


# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'games_played',
                    'wins', 'draws', 'losses', 'goals_for',
                    'goals_against', 'points', 'logo')
    search_fields = ['name']


class FixtureAdmin(admin.ModelAdmin):
    list_display = ('opponent', 'date', 'time', 'home_or_away',
                    'location', 'goals_for',
                    'goals_against', 'match_completed')
    list_filter = ('date', 'home_or_away',
                   'match_completed')  # Allows filtering
    search_fields = ['opponent', 'location']


admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Profile)
