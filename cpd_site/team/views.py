from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Fixture, Profile, ManagerPost, PlayerAvailability
from .forms import ManagerPostForm, PlayerAvailabilityForm, ProfileForm


def home(request):
    """Fetches team details, next fixture, latest result, and league table"""
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

    # Extract top team and CPD position
    top_team = league_table.first()  # First team (highest points)
    cpd_team = league_table.filter(name="CPD Yr Wyddgrug").first()

    # Find CPD position in league
    cpd_position = list(league_table).index(cpd_team) + 1 if cpd_team else None

    # Fetch top 3 teams
    top_teams = Team.objects.all().order_by('-points', '-goals_for', 'goals_against')[:3]

    # Ensure CPD Yr Wyddgrug is included even if not in top 3
    cpd_team = Team.objects.filter(name="CPD Yr Wyddgrug").first()

    if cpd_team and cpd_team not in top_teams:
        league_table = list(top_teams) + [cpd_team]
    else:
        league_table = list(top_teams)

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

    # Manager can make announcements
    if request.method == "POST":
        form = ManagerPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.manager = request.user
            post.save()
    else:
        form = ManagerPostForm()

    posts = ManagerPost.objects.all().order_by("-created_at")

    # Get all upcoming fixtures
    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by("date", "time")

    # Create a dictionary mapping each fixture to player availability
    fixture_availability = {
        fixture: PlayerAvailability.objects.filter(fixture=fixture)
        for fixture in upcoming_fixtures
    }

    return render(request, "team/manager_dashboard.html", {
        "form": form,
        "posts": posts,
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability
    })


@login_required
def player_dashboard(request):
    """View for player-specific actions, including setting availability."""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("create_profile")

    if user_profile.role != "player":
        return render(request, "team/access_denied.html")

    if request.method == "POST":
        form = PlayerAvailabilityForm(request.POST)
        if form.is_valid():
            fixture = form.cleaned_data["fixture"]
            status = form.cleaned_data["status"]

            # **Check if player has already submitted availability for this fixture**
            availability, created = PlayerAvailability.objects.update_or_create(
                player=request.user, fixture=fixture,
                defaults={"status": status}
            )

    else:
        form = PlayerAvailabilityForm()

    availabilities = PlayerAvailability.objects.filter(player=request.user)

    return render(request, "team/player_dashboard.html", {
        "form": form, "availabilities": availabilities})


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
