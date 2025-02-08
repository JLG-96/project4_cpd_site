from django.shortcuts import render
from .models import Team, Fixture


def homepage(request):
    """ Fetches team details, next fixture, latest result, and league table """

    team = Team.objects.first()

    # Fetch upcoming fixture (if any)
    upcoming_fixture = Fixture.objects.filter(
        match_completed=False).order_by('date', 'time').first()

    # Fetch the latest completed match (most recent)
    latest_result = Fixture.objects.filter(
        match_completed=True).order_by('-date', '-time').first()

    # Fetch full league table (ordered by points, goal difference, goals for)
    league_table = Team.objects.all().order_by(
        '-points', '-goals_for', 'goals_against')
    
    # Extract top team and CPD postition
    top_team = league_table.first()  # First team (highest points)
    cpd_team = league_table.filter(name="CPD Yr Wyddgrug").first()

    # Find CPD position in league
    cpd_position = list(league_table).index(cpd_team) + 1 if cpd_team else None

    # Manager's latest comment (Replace with dynamic content later)
    managers_comment = "Looking forward to the next game!"

    context = {
        "team": team,
        "upcoming_fixture": upcoming_fixture,
        "latest_result": latest_result,
        "top_team": top_team,
        "cpd_team": cpd_team,
        "cpd_position": cpd_position,
        "league_table": league_table,
        "managers_comment": managers_comment
    }

    return render(request, "team/homepage.html", context)


def results_view(request):
    """View for displaying past match results"""
    past_fixtures = Fixture.objects.filter(
        match_completed=True).order_by('-date', '-time')

    context = {
        "past_fixtures": past_fixtures
    }

    return render(request, "team/results.html", context)


def fixtures_view(request):
    """View to display upcoming fixtures"""
    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False).order_by('date', 'time')

    # Debugging print 
    print("upcoming fixtures:", upcoming_fixtures)

    context = {
        "upcoming_fixtures": upcoming_fixtures
    }

    return render(request, "team/fixtures.html", context)


def league_table(request):
    """ Orders teams by points then by goal difference. """
    teams = Team.objects.all().order_by(
        '-points', '-goals_for', 'goals_against')

    return render(request, 'team/league_table.html', {'teams': teams})
