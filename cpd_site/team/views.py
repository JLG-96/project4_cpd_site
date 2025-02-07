from django.shortcuts import render
from .models import Team, Fixture


def homepage(request):
    """ Fetches team details, next fixture, latest result, and league table """
    
    team = Team.objects.first()

    # Fetch upcoming fixture (if any)
    upcoming_fixture = Fixture.objects.filter(match_completed=False).order_by('date', 'time').first()

    # Fetch the latest completed match (most recent)
    latest_result = Fixture.objects.filter(match_completed=True).order_by('-date', '-time').first()

    # Example league table (Replace with real data later)
    league_table = [
        {"position": 1, "team": "Top Team FC", "points": 50},
        {"position": 2, "team": "CPD Yr Wyddgrug", "points": 48},
    ]

    # Manager's latest comment (Replace with dynamic content later)
    managers_comment = "Looking forward to the next game! The team is training hard."

    context = {
        "team": team,
        "upcoming_fixture": upcoming_fixture,
        "latest_result": latest_result,  
        "league_table": league_table,
        "managers_comment": managers_comment
    }

    return render(request, "team/homepage.html", context)


def results_view(request):
    """View for displaying past match results"""
    past_fixtures = Fixture.objects.filter(match_completed=True).order_by('-date', '-time')

    context = {
        "past_fixtures": past_fixtures
    }

    return render(request, "team/results.html", context)


def fixtures_view(request):
    """View to display upcoming fixtures"""
    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by('date', 'time')

    #debugging print 
    print("upcoming fixtures:", upcoming_fixtures)

    context = {
        "upcoming_fixtures": upcoming_fixtures
    }

    return render(request, "team/fixtures.html", context)


def league_table(request):
    # Orders teams by pointes then by goal difference.
    teams = Team.objects.all().order_by('-points', '-goals_for', 'goals_against')
    return render(request, 'team/league_table.html', {'teams': teams})