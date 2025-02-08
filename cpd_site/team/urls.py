from django.urls import path
from .views import homepage, results_view, fixtures_view, league_table
from .views import manager_dashboard, player_dashboard, create_profile


urlpatterns = [
    path('', homepage, name='home'),
    path('results/', results_view, name='results'), 
    path('fixtures/', fixtures_view, name='fixtures'),
    path('table/', league_table, name='league_table'),
    path("manager-dashboard/", manager_dashboard, name="manager_dashboard"),
    path("player-dashboard/", player_dashboard, name="player_dashboard"),
    path("create-profile/", create_profile, name="create_profile"),
]
