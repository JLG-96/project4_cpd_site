from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import (Team,
                     Fixture,
                     Profile,
                     PlayerAvailability,
                     ManagerMessage,
                     ManagerMessageComment)
from .forms import (ProfileForm,
                    ManagerPostForm,
                    ManagerPost,
                    ManagerMessageForm,
                    ManagerMessageCommentForm)
from django.contrib import messages


def home(request):
    """Fetches team details, upcoming fixture, and league standings."""

    # Fetch the team
    team = Team.objects.filter(name="CPD Yr Wyddgrug").first()

    # Fetch upcoming fixture
    upcoming_fixture = Fixture.objects.filter(
        match_completed=False).order_by('date', 'time').first()

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
def player_dashboard(request):
    """View for player-specific actions, including setting availability and 
        commenting on manager messages."""

    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("create_profile")

    if user_profile.role != "player":
        return render(request, "team/access_denied.html")

    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False).order_by("date", "time")

    # Fetch latest messages from the manager (only last 5 messages)
    manager_messages = ManagerMessage.objects.prefetch_related(
        "comments").order_by("-created_at")[:5]

    # Handle comment submission
    if request.method == "POST" and "submit_comment" in request.POST:
        message_id = request.POST.get("message_id")
        message = get_object_or_404(ManagerMessage, id=message_id)
        comment_form = ManagerMessageCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.player = request.user
            comment.message = message
            comment.save()
            return redirect("player_dashboard")

    else:
        comment_form = ManagerMessageCommentForm()

    fixture_availability = {
        pa.fixture.id: pa.status for pa in PlayerAvailability.objects.filter(
            player=request.user)
    }

    return render(request, "team/player_dashboard.html", {
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability,
        "manager_messages": manager_messages,  # Messages with comments
        "comment_form": comment_form,  # Form for submitting comments
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
    past_fixtures = Fixture.objects.filter(match_completed=True).order_by(
        '-date', '-time')

    return render(request, "team/results.html", {
        "past_fixtures": past_fixtures})


def fixtures_view(request):
    """View to display only upcoming fixtures."""
    upcoming_fixtures = Fixture.objects.filter(match_completed=False).order_by(
        "date", "time")
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
    """View for manager-specific actions."""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("create_profile")

    if user_profile.role != "manager":
        return render(request, "team/access_denied.html")

    # Handling manager posts
    if request.method == "POST" and "post_announcement" in request.POST:
        post_form = ManagerPostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.manager = request.user
            post.save()

    else:
        post_form = ManagerPostForm()

    # Handling messages to players
    if request.method == "POST" and "send_message" in request.POST:
        message_form = ManagerMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.manager = request.user
            message.save()
            return redirect("manager_dashboard")

    else:
        message_form = ManagerMessageForm()

    # Fetch all manager posts and messages
    posts = ManagerPost.objects.all().order_by("-created_at")
    sent_messages = ManagerMessage.objects.prefetch_related(
        "comments").order_by("-created_at")

    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False).order_by("date", "time")

    fixture_availability = {
        fixture.id: list(PlayerAvailability.objects.filter(fixture=fixture))
        for fixture in upcoming_fixtures
    }

    return render(
        request,
        "team/manager_dashboard.html",
        {
            "post_form": post_form,
            "posts": posts,
            "message_form": message_form,
            "sent_messages": sent_messages,
            "upcoming_fixtures": upcoming_fixtures,
            "fixture_availability": fixture_availability,
        },
    )


@login_required
def edit_comment(request, comment_id):
    """Allows players to edit their own comments."""
    comment = get_object_or_404(ManagerMessageComment, id=comment_id)

    if request.user != comment.player:
        return redirect("player_dashboard")  # Prevent unauthorized access

    if request.method == "POST":
        form = ManagerMessageCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("player_dashboard")  # Redirect back after editing

    else:
        form = ManagerMessageCommentForm(instance=comment)

    return render(request, "team/edit_comment.html", {
        "form": form, "comment": comment})


@login_required
def delete_comment(request, comment_id):
    """Allows players to delete their own comments."""
    comment = get_object_or_404(ManagerMessageComment, id=comment_id)

    if request.user == comment.player:
        comment.delete()

    return redirect("player_dashboard")  # Redirect back after deletion
