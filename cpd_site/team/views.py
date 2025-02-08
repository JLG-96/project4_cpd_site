from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Fixture, Profile, ManagerPost, PlayerAvailability
from .forms import ManagerPostForm, PlayerAvailabilityForm, ProfileForm
from django.contrib import messages


def home(request):
    """Fetches team details, upcoming fixture, and league standings."""

    # Always fetch CPD Yr Wyddgrug
    team = Team.objects.filter(name="CPD Yr Wyddgrug").first()

    # Fetch upcoming fixture
    upcoming_fixture = Fixture.objects.filter(
        match_completed=False
    ).order_by('date', 'time').first()

    # Fetch league standings (ALREADY WORKING, DON'T CHANGE)
    league_table = Team.objects.all().order_by('-points', '-goals_for', 'goals_against')

    # Find CPD's actual position in the league
    cpd_team = Team.objects.filter(name="CPD Yr Wyddgrug").first()
    cpd_position = list(league_table).index(cpd_team) + 1 if cpd_team else None

    # Get top 3 teams
    top_teams = list(league_table[:3])

    # Ensure CPD is included at the correct position
    league_preview = [{"position": i + 1, "name": t.name, "points": t.points} for i, t in enumerate(top_teams)]
    if cpd_team and cpd_team not in top_teams:
        league_preview.append({"position": cpd_position, "name": cpd_team.name, "points": cpd_team.points})

    context = {
        "team": team,
        "upcoming_fixture": upcoming_fixture,
        "league_preview": league_preview,
    }

    return render(request, "team/home.html", context)


@login_required
def manager_dashboard(request):
    """View for manager-specific actions"""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("create_profile")

    if user_profile.role != "manager":
        return render(request, "team/access_denied.html")

    # Fetch upcoming fixtures
    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by("date", "time")

    # Create fixture availability dictionary
    fixture_availability = {}
    for fixture in upcoming_fixtures:
        fixture.formatted_date = format(fixture.date, "d/m/Y")
        fixture_availability[fixture] = {
            "available": PlayerAvailability.objects.filter(fixture=fixture, status="yes"),
            "not_available": PlayerAvailability.objects.filter(fixture=fixture, status="no"),
        }

    context = {
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability or {},  # Always ensure it's a dictionary
    }

    return render(request, "team/manager_dashboard.html", context)


@login_required
@login_required
def player_dashboard(request):
    """View for player-specific actions, including setting availability."""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("create_profile")

    if user_profile.role != "player":
        return render(request, "team/access_denied.html")

    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by("date", "time")

    # Get existing availability for the logged-in player
    fixture_availability = {pa.fixture.id: pa.status for pa in PlayerAvailability.objects.filter(player=request.user)}

    if request.method == "POST":
        for fixture in upcoming_fixtures:
            availability_status = request.POST.get(f"availability_{fixture.id}")
            if availability_status:
                PlayerAvailability.objects.update_or_create(
                    player=request.user, fixture=fixture,
                    defaults={"status": availability_status}
                )
        messages.success(request, "Availability updated successfully.")
        return redirect("player_dashboard")

    return render(request, "team/player_dashboard.html", {
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability
    })


@login_required
def create_profile(request):
    """Allows users to create a profile if they don’t have one."""
    if Profile.objects.filter(user=request.user).exists():
        return redirect("home")

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("manager_dashboard" if profile.role == "manager" else "player_dashboard")
    else:
        form = ProfileForm()

    return render(request, "team/create_profile.html", {"form": form})


def results_view(request):
    """View for displaying past match results"""
    past_fixtures = Fixture.objects.filter(
        match_completed=True).order_by('-date', '-time')

    return render(request, "team/results.html", {"past_fixtures": past_fixtures})


def fixtures_view(request):
    """View to display only upcoming fixtures."""
    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by("date", "time")
    return render(request, "team/fixtures.html", {"upcoming_fixtures": upcoming_fixtures})


def league_table(request):
    """View for displaying league table standings."""
    teams = Team.objects.all().order_by('-points', '-goals_for', 'goals_against')
    return render(request, 'team/league_table.html', {'teams': teams})
