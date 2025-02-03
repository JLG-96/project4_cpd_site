from django.urls import path
from .views import homepage, results_view

urlpatterns = [
    path('', homepage, name='homepage'),
    path('results/', results_view, name='results'),  
]
