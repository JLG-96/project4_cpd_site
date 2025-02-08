from django.urls import path
from .views import home, results_view, fixtures_view, league_table
from .views import manager_dashboard, player_dashboard, create_profile
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name='home'),
    path('results/', results_view, name='results'), 
    path('fixtures/', fixtures_view, name='fixtures'),
    path('table/', league_table, name='league_table'),
    path("manager-dashboard/", manager_dashboard, name="manager_dashboard"),
    path("player-dashboard/", player_dashboard, name="player_dashboard"),
    path("create-profile/", create_profile, name="create_profile"),
    path("accounts/logout/", LogoutView.as_view(next_page="home"), name="logout"),
    ]
