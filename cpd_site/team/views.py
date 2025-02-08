from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Fixture, Profile, ManagerPost, PlayerAvailability
from .forms import ManagerPostForm, PlayerAvailabilityForm, ProfileForm


def home(request):
    """Fetches team details, next fixture, latest result, and league table"""
    # Fetch full league table ordered correctly
    league_table = list(Team.objects.all().order_by('-points', '-goals_for', 'goals_against'))

    # Fetch CPD Yr Wyddgrug team and find its actual position
    cpd_team = Team.objects.filter(name="CPD Yr Wyddgrug").first()
    cpd_position = None

    if cpd_team in league_table:
        cpd_position = league_table.index(cpd_team) + 1  # Get CPD's actual position

    # Extract top 3 teams from the league
    top_teams = league_table[:3] if len(league_table) >= 3 else league_table

    # Pass the entire league table but only display needed parts in HTML
    context = {
        "league_table": league_table,  # Full league table
        "top_teams": top_teams,  # Top 3 teams
        "cpd_team": cpd_team,  # CPD Yr Wyddgrug
        "cpd_position": cpd_position,  #  CPD’s actual position
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

    # Fetch upcoming fixtures & player availability **ONLY FOR UPCOMING FIXTURES**
    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by("date", "time")
    player_availability = PlayerAvailability.objects.filter(fixture__match_completed=False)

    return render(request, "team/manager_dashboard.html", {
        "form": form,
        "posts": posts,
        "upcoming_fixtures": upcoming_fixtures,
        "player_availability": player_availability
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
