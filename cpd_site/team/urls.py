from django.urls import path
from .views import homepage, results_view, fixtures_view, league_table

urlpatterns = [
    path('', homepage, name='homepage'),
    path('results/', results_view, name='results'), 
    path('fixtures/', fixtures_view, name='fixtures'),
    path('table/', league_table, name='league_table'),
]
