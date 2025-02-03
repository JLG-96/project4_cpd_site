from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Team  # Import your models (add others when created)

def homepage(request):
    # Fetch CPD Yr Wyddgrug team data (assumes only one team for now)
    team = Team.objects.first()

    # Dummy data for upcoming fixture & league table (replace later with real models)
    upcoming_fixture = {
        "home_team": "CPD Yr Wyddgrug",
        "away_team": "Opponent FC",
        "date": "2025-02-10",
        "time": "15:00",
        "location": "Home Ground"
    }
    
    league_table = [
        {"position": 1, "team": "Top Team FC", "points": 50},
        {"position": 2, "team": "CPD Yr Wyddgrug", "points": 48},  # Example standing
    ]

    # Dummy manager's comment
    managers_comment = "Looking forward to the next game! The team is training hard."

    # Pass data to the template
    context = {
        "team": team,
        "upcoming_fixture": upcoming_fixture,
        "league_table": league_table,
        "managers_comment": managers_comment
    }

    return render(request, "team/homepage.html", context)
