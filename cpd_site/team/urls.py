from django.urls import path
from .views import homepage, fixtures_view, results_view

urlpatterns = [
    path('', homepage, name='homepage'),
        path('fixtures/', fixtures_view, name='fixtures'),
    path('results/', results_view, name='results'),
]
