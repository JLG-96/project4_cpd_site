from django.shortcuts import render
from .models import Team, Fixture

# Create your views here.
def homepage(request):
    # Fetch CPD Yr Wyddgrug team details
    team = Team.objects.first()

    # Fetch the next upcoming fixture from the database
    upcoming_fixture = Fixture.objects.filter(is_played=False).order_by('date', 'time').first()

    # Fetch the most recent past result
    latest_result = Fixture.objects.filter(is_played=True).order_by('-date', '-time').first()

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


def results_view(request):
    """View to display past match results"""
    past_fixtures = Fixture.objects.filter(is_played=True).order_by('-date', '-time')  # Show most recent first

    context = {
        "past_fixtures": past_fixtures
    }

    return render(request, "team/results.html", context)


def fixtures_view(request):
    """View to display upcoming fixtures"""
    upcoming_fixtures = Fixture.objects.filter(is_played=False).order_by('date', 'time')

    context = {
        "upcoming_fixtures": upcoming_fixtures
    }

    return render(request, "team/fixtures.html", context)
