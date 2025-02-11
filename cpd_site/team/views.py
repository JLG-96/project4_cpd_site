from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Fixture, Profile, PlayerAvailability, ManagerMessage
from .forms import (ProfileForm,
                    ManagerPostForm,
                    ManagerPost,
                    ManagerMessageForm)
from django.contrib import messages


def home(request):
    """Fetches team details, upcoming fixture, and league standings."""

    # Fetch the team
    team = Team.objects.filter(name="CPD Yr Wyddgrug").first()

    # Fetch upcoming fixture
    upcoming_fixture = Fixture.objects.filter(
        match_completed=False
    ).order_by('date', 'time').first()

    # Fetch league standings
    league_table = Team.objects.all().order_by(
        '-points', '-goals_for', 'goals_against')

    # Find CPD's actual position in the league
    cpd_team = Team.objects.filter(name="CPD Yr Wyddgrug").first()
    cpd_position = list(league_table).index(cpd_team) + 1 if cpd_team else None

    # Get top 3 teams
    top_teams = list(league_table[:3])

    # Ensure CPD is included at the correct position
    league_preview = [{
        "position": i + 1, "name": t.name, "points": t.points} for i,
        t in enumerate(top_teams)]
    if cpd_team and cpd_team not in top_teams:
        league_preview.append({
            "position": cpd_position, "name": cpd_team.name,
            "points": cpd_team.points})

    # Fetch only the last 5 manager posts
    manager_posts = ManagerPost.objects.order_by("-created_at")[:5]

    print("Manager Posts Retrieved:", manager_posts)  # Debugging line

    context = {
        "team": team,
        "upcoming_fixture": upcoming_fixture,
        "league_preview": league_preview,
        "manager_posts": manager_posts,  # Pass multiple posts
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

    if request.method == "POST":
        form = ManagerPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.manager = request.user
            post.save()
    else:
        form = ManagerPostForm()

    posts = ManagerPost.objects.all().order_by("-created_at")

    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by(
        "date", "time")

    fixture_availability = {}
    for fixture in upcoming_fixtures:
        fixture_availability[fixture.id] = list(
            PlayerAvailability.objects.filter(fixture=fixture))

    # Debugging: Print data to console
    print("Upcoming Fixtures:", upcoming_fixtures)
    print("Fixture Availability:", fixture_availability)

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

    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by(
        "date", "time")

    # Get existing availability for the logged-in player
    fixture_availability = {
        pa.fixture.id: pa.status for pa in PlayerAvailability.objects.filter(
            player=request.user)}

    if request.method == "POST":
        for fixture in upcoming_fixtures:
            availability_status = request.POST.get(
                f"availability_{fixture.id}")
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
    """Allows users to create a profile if they don't have one."""
    if Profile.objects.filter(user=request.user).exists():
        return redirect("home")

    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect(
                "manager_dashboard" if profile.role ==
                "manager" else "player_dashboard")
    else:
        form = ProfileForm()

    return render(request, "team/create_profile.html", {"form": form})


def results_view(request):
    """View for displaying past match results"""
    past_fixtures = Fixture.objects.filter(
        match_completed=True).order_by('-date', '-time')

    return render(request, "team/results.html", {
        "past_fixtures": past_fixtures})


def fixtures_view(request):
    """View to display only upcoming fixtures."""
    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False).order_by("date", "time")
    return render(request, "team/fixtures.html", {
        "upcoming_fixtures": upcoming_fixtures})


def league_table(request):
    """View for displaying league table standings."""
    teams = Team.objects.all().order_by(
        '-points', '-goals_for', 'goals_against')
    return render(request, 'team/league_table.html', {'teams': teams})


@login_required
def edit_manager_post(request, post_id):
    post = get_object_or_404(ManagerPost, id=post_id)

    # Ensure only the manager who created the post can edit it
    if request.user != post.manager:
        return redirect("manager_dashboard")

    if request.method == "POST":
        form = ManagerPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redirect to homepage after saving

    else:
        form = ManagerPostForm(instance=post)

    return render(request, "team/edit_manager_post.html", {
        "form": form, "post": post})


@login_required
def manager_dashboard(request):
    """View for manager-specific actions"""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("create_profile")

    if user_profile.role != "manager":
        return render(request, "team/access_denied.html")

    # Forms for posts & messages
    post_form = ManagerPostForm()
    message_form = ManagerMessageForm()

    if request.method == "POST":
        if "post_submit" in request.POST:  # Check if it's a comment submission
            post_form = ManagerPostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.manager = request.user
                post.save()
                return redirect("manager_dashboard")

        elif "message_submit" in request.POST:
            message_form = ManagerMessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.manager = request.user
                message.save()
                return redirect("manager_dashboard")

    # Fetch posts & messages
    posts = ManagerPost.objects.all().order_by("-created_at")
    messages = ManagerMessage.objects.all().order_by("-created_at")

    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False).order_by("date", "time")
    fixture_availability = {fixture.id: list(
        PlayerAvailability.objects.filter(
            fixture=fixture)) for fixture in upcoming_fixtures}

    return render(request, "team/manager_dashboard.html", {
        "post_form": post_form,
        "message_form": message_form,
        "posts": posts,
        "messages": messages,
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability,
    })
