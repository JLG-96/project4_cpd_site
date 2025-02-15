from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import (Team,
                     Fixture,
                     Profile,
                     PlayerAvailability,
                     ManagerMessage,
                     ManagerMessageComment,
                     Notification)
from .forms import (ProfileForm,
                    ManagerPostForm,
                    ManagerPost,
                    ManagerMessageForm,
                    ManagerMessageCommentForm)


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


def create_notification(recipient, type, message, link=None):
    """Creates a new notification for the given recipient."""
    Notification.objects.create(
        recipient=recipient,
        type=type,
        message=message,
        link=link
    )


@login_required
def player_dashboard(request):
    """View for player-specific actions including setting availability,
    commenting on manager messages, and viewing notifications."""

    if request.user.profile.role != "player":
        return redirect("home")

    # Fetch notifications for the logged-in player (not admin)
    notifications = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).order_by("-created_at")

    # Fetch upcoming fixtures
    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False
    ).order_by("date", "time")

    # Get ordered league table and assign league positions
    league_table = Team.objects.all().order_by('-points', '-goals_for', 'goals_against')

    for fixture in upcoming_fixtures:
        opponent_team = fixture.opponent
        if opponent_team:
            try:
                opponent_team.league_position = (
                    list(league_table).index(opponent_team) + 1
                )
            except ValueError:
                opponent_team.league_position = None  # If team isn't found in the league table

    # Fetch latest manager messages (only last 5 messages)
    manager_messages = ManagerMessage.objects.prefetch_related(
        "comments"
    ).order_by("-created_at")[:5]

    # Handle player availability submission
    if request.method == "POST" and "set_availability" in request.POST:
        fixture_id = request.POST.get("fixture_id")
        status = request.POST.get("status")  # 'yes' or 'no'

        fixture = get_object_or_404(Fixture, id=fixture_id)
        availability, created = PlayerAvailability.objects.update_or_create(
            player=request.user,
            fixture=fixture,
            defaults={"status": status}
        )

        # Notify the manager
        manager = User.objects.filter(profile__role="manager").first()
        if manager:
            Notification.objects.create(
                recipient=manager,
                type="availability",
                message=f"{request.user.username} has updated availability for {fixture.opponent}.",
                link="/manager-dashboard/"
            )

        return redirect("player_dashboard")

    # Handle comment submission on manager messages
    if request.method == "POST" and "submit_comment" in request.POST:
        message_id = request.POST.get("message_id")
        message = get_object_or_404(ManagerMessage, id=message_id)
        comment_form = ManagerMessageCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.player = request.user
            comment.message = message
            comment.save()

            # Notify the manager of the new comment
            create_notification(
                recipient=message.manager,
                type="comment",
                message=f"{request.user.username} has commented on your message: {message.title}.",
                link="/manager-dashboard/"
            )

            return redirect("player_dashboard")
    else:
        comment_form = ManagerMessageCommentForm()

    # Fetch player availability correctly
    fixture_availability = {
        fixture.id: PlayerAvailability.objects.filter(
            player=request.user, fixture=fixture
        ).first()
        for fixture in upcoming_fixtures
    }

    return render(request, "team/player_dashboard.html", {
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability,
        "manager_messages": manager_messages,
        "comment_form": comment_form,
        "notifications": notifications,
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
    """View for manager actions."""

    if request.user.profile.role != "manager":
        return redirect("home")

    # Fetch only notifications meant for the manager
    notifications = Notification.objects.filter(
        recipient__profile__role="manager",
        is_read=False
        ).order_by("-created_at")

    print("🔍 Manager Notifications:", notifications)  # Debugging

    # Ensure form variables are defined outside of the if-block
    post_form = ManagerPostForm()
    message_form = ManagerMessageForm()

    # Manager posts announcements
    if request.method == "POST" and "post_announcement" in request.POST:
        post_form = ManagerPostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.manager = request.user
            post.save()

    # Manager sends messages to players
    if request.method == "POST" and "send_message" in request.POST:
        message_form = ManagerMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.manager = request.user
            message.save()
            print(" Manager Message Sent:", message)  # Debugging

            # Notify all players
            players = User.objects.filter(profile__role="player")
            for player in players:
                create_notification(
                    recipient=player,
                    type="message",
                    message="Your manager has sent a new message.",
                    link="/player-dashboard/"
                )

            return redirect("manager_dashboard")

    # Fetch manager posts and sent messages
    posts = ManagerPost.objects.all().order_by("-created_at")
    sent_messages = ManagerMessage.objects.all().order_by("-created_at")

    # Fetch upcoming fixtures
    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False).order_by("date", "time")

    fixture_availability = {
        fixture.id: list(PlayerAvailability.objects.filter(fixture=fixture))
        for fixture in upcoming_fixtures
    }

    return render(request, "team/manager_dashboard.html", {
        "post_form": post_form,
        "message_form": message_form,  # Now it will always exist
        "posts": posts,
        "sent_messages": sent_messages,
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability,
        "notifications": notifications,
    })


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


@login_required
def mark_notification_read(request, notification_id):
    """Marks a notification as read and keeps user on dashboard."""
    notification = get_object_or_404(Notification, id=notification_id)

    if request.method == "POST":
        notification.is_read = True
        notification.save()

        # Determine correct redirect
        next_page = request.POST.get("next")
        if not next_page:
            if request.user.profile.role == "manager":
                next_page = "manager_dashboard"
            else:
                next_page = "player_dashboard"

        return redirect(next_page)

    print(f"📩 Marking notification {notification_id} as read...")


@login_required
def edit_manager_message(request, message_id):
    """Allows the manager to edit a message sent to players."""
    message = get_object_or_404(ManagerMessage, id=message_id)

    # Ensure only the manager who created the message can edit it
    if request.user != message.manager:
        return redirect("manager_dashboard")

    if request.method == "POST":
        form = ManagerMessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect("manager_dashboard")  # Redirect back after editing

    else:
        form = ManagerMessageForm(instance=message)

    return render(request, "team/edit_manager_message.html", {
        "form": form, "message": message})


@login_required
def delete_manager_message(request, message_id):
    """Allows the manager to delete a message sent to players."""
    message = get_object_or_404(ManagerMessage, id=message_id)

    # Debugging: Print the current user and role
    print(f"🗑 Attempting to delete message: {message.title}")
    print(f"👤 Current User: {request.user.username}, Role: {request.user.profile.role}")

    # Ensure only the manager who created the message can delete it
    if request.user.profile.role != "manager":
        print("Unauthorized deletion attempt!")
        return redirect("manager_dashboard")

    message.delete()
    print("Message deleted successfully!")
    return redirect("manager_dashboard")
