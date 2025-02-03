from django.shortcuts import render
from .models import Team, Fixture

# Create your views here.
def homepage(request):
    # Fetch CPD Yr Wyddgrug team details
    team = Team.objects.first()

    # Fetch the next upcoming fixture from the database
    upcoming_fixture = Fixture.objects.filter(is_played=False).order_by('date', 'time').first()

    # Dummy league table (will be replaced later)
    league_table = [
        {"position": 1, "team": "Top Team FC", "points": 50},
        {"position": 2, "team": "CPD Yr Wyddgrug", "points": 48},  # Example standing
    ]

    managers_comment = "Looking forward to the next game! The team is training hard."

    context = {
        "team": team,
        "upcoming_fixture": upcoming_fixture,  # Now using real database data
        "league_table": league_table,
        "managers_comment": managers_comment
    }

    return render(request, "team/homepage.html", context)
