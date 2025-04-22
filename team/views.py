from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import (Team,
                     Fixture,
                     PlayerAvailability,
                     ManagerMessage,
                     ManagerMessageComment,
                     Notification,
                     Profile)
from .forms import (ManagerPostForm,
                    ManagerPost,
                    ManagerMessageForm,
                    ManagerMessageCommentForm,
                    CustomUserRegistrationForm)
from django.utils.timezone import now
from django.utils import timezone


def home(request):
    """Fetches team details, upcoming fixture, recent result, and league."""

    # Fetch the team
    team = Team.objects.filter(name="CPD Yr Wyddgrug").first()

    # Fetch upcoming fixture (Exclude past fixtures)
    upcoming_fixture = Fixture.objects.filter(
        match_completed=False,
        date__gte=now().date()  # Only include fixtures today or in the future
    ).order_by("date", "time").first()

    # Fetch the most recent completed match
    latest_result = Fixture.objects.filter(
        match_completed=True
    ).order_by("-date", "-time").first()

    # Fetch league standings
    league_table = Team.objects.all().order_by(
        "-points", "-goals_for", "goals_against"
    )

    # Find CPD's actual position in the league
    cpd_team = next((
        t for t in league_table if t.name == "CPD Yr Wyddgrug"), None)
    cpd_position = (
        list(league_table).index(cpd_team) + 1 if cpd_team else None
    )

    # Get top 3 teams
    top_teams = list(league_table[:3])

    # Ensure CPD is included at the correct position
    league_preview = [
        {"position": i + 1, "name": t.name, "points": t.points}
        for i, t in enumerate(top_teams)
    ]
    if cpd_team and cpd_team not in top_teams:
        league_preview.append(
            {
                "position": cpd_position,
                "name": cpd_team.name,
                "points": cpd_team.points,
            }
        )

    # Fetch exactly the last 5 manager posts (newest first)
    manager_posts = ManagerPost.objects.order_by("-created_at")[:5]

    context = {
        "team": team,
        "upcoming_fixture": upcoming_fixture,
        "latest_result": latest_result,  # Now passing latest result
        "league_preview": league_preview,
        "manager_posts": manager_posts,  # Pass all posts for cycling
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

    # Fetch notifications for the logged-in player
    notifications = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).order_by("-created_at")

    # Fetch upcoming fixtures
    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False,
        date__gte=now().date()  # Only include future fixtures
    ).order_by("date", "time")

    # Fetch league table
    league_table = Team.objects.all().order_by(
        '-points', '-goals_for', 'goals_against')

    # Assign league position dynamically
    for fixture in upcoming_fixtures:
        opponent_team = fixture.opponent
        if opponent_team:
            try:
                opponent_team.league_position = (
                    list(league_table).index(opponent_team) + 1
                )
            except ValueError:
                opponent_team.league_position = None

    # Fetch latest manager messages WITH comments
    manager_messages = ManagerMessage.objects.prefetch_related(
        "comments").order_by("-created_at")[:5]
    # Handle comment submissions
    if request.method == "POST" and "submit_comment" in request.POST:
        message_id = request.POST.get("message_id")
        message = get_object_or_404(ManagerMessage, id=message_id)

        form = ManagerMessageCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.player = request.user
            comment.message = message
            comment.save()
            return redirect("player_dashboard")

    # Handle player availability submission
    if request.method == "POST" and "set_availability" in request.POST:
        fixture_id = request.POST.get("fixture_id")
        status = request.POST.get("status")  # 'yes' or 'no'

        fixture = get_object_or_404(Fixture, id=fixture_id)
        PlayerAvailability.objects.update_or_create(
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
                message=f"{
                    request.user.username} has updated availability for {
                        fixture.opponent}.",
                link="/manager-dashboard/"
            )

        return redirect("player_dashboard")

    # Fetch player availability
    fixture_availability = {
        fixture.id: PlayerAvailability.objects.filter(
            player=request.user, fixture=fixture
        ).first()
        for fixture in upcoming_fixtures
    }

    return render(request, "team/player_dashboard.html", {
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability,
        "notifications": notifications,
        "manager_messages": manager_messages,
        "comment_form": ManagerMessageCommentForm(),
    })


def results_view(request):
    """
    Return a view displaying all previously played fixtures,
    ordered by most recent first.
    """
    past_fixtures = Fixture.objects.filter(match_completed=True).order_by(
        '-date', '-time')

    return render(request, "team/results.html", {
        "past_fixtures": past_fixtures})


def fixtures_view(request):
    """View to display only upcoming fixtures."""
    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False,
        date__gte=now().date()  # Only show future fixtures
    ).order_by("date", "time")
    return render(request, "team/fixtures.html", {
        "upcoming_fixtures": upcoming_fixtures})


def league_table(request):
    """
    Return a view displaying the league table standings,
    ordered by points, goals for, and goals against.
    """
    teams = Team.objects.all().order_by(
        '-points', '-goals_for', 'goals_against')
    return render(request, 'team/league_table.html', {'teams': teams})


def register_user(request):
    """
    Handle user registration for players and managers
    using an invite code. Creates a matching Profile after User.
    """
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data["role"]

            # Create the associated profile with selected role
            Profile.objects.create(user=user, role=role)

            return redirect("login")
        # Redirect to login page after registration
    else:
        form = CustomUserRegistrationForm()

    return render(request, "team/register.html", {"form": form})


@login_required
def edit_manager_post(request, post_id):
    """View to edit a specific manager's post."""
    post = get_object_or_404(ManagerPost, id=post_id)  # Fetch correct post

    if request.method == "POST":
        form = ManagerPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redirect back to homepage

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

    # Ensure form variables are defined outside of the if-block
    post_form = ManagerPostForm()
    message_form = ManagerMessageForm()

    # Manager posts announcements
    if request.method == "POST" and "post_announcement" in request.POST:
        announcement_content = request.POST.get("announcement")

        if announcement_content:
            # Create a new post
            ManagerPost.objects.create(
                manager=request.user,
                title="Manager's Comments",
                content=announcement_content,
                created_at=timezone.now()
            )

            # Keep only the last 5 posts
            all_posts = ManagerPost.objects.order_by("-created_at")
            if all_posts.count() > 5:
                for post in all_posts[5:]:  # Get all older posts beyond 5
                    post.delete()  # Delete them

            return redirect("manager_dashboard")

    # Manager sends messages to players
    if request.method == "POST" and "send_message" in request.POST:
        message_form = ManagerMessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.manager = request.user
            message.save()

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

    # Fetch only the latest announcement
    latest_post = ManagerPost.objects.all().order_by("-created_at").first()

    # Fetch sent messages
    sent_messages = ManagerMessage.objects.prefetch_related(
        "comments").order_by("-created_at")

    # Fetch upcoming fixtures
    upcoming_fixtures = Fixture.objects.filter(
        match_completed=False,
        date__gte=now().date()  # Exclude past fixtures
    ).order_by("date", "time")

    # Fetch ordered league table
    league_table = list(Team.objects.all().order_by(
        '-points', '-goals_for', 'goals_against'
    ))

    # Assign league position dynamically
    for index, team in enumerate(league_table, start=1):
        team.league_position = index

    # Ensure upcoming fixtures display correct opponent league positions
    for fixture in upcoming_fixtures:
        opponent_team = fixture.opponent
        if opponent_team:
            opponent_team.league_position = next(
                (team.league_position for team in league_table if team.id ==
                    opponent_team.id),
                None
            )

    fixture_availability = {
        fixture.id: list(PlayerAvailability.objects.filter(fixture=fixture))
        for fixture in upcoming_fixtures
    }

    posts = ManagerPost.objects.exclude(id=None).order_by("-created_at")
    return render(request, "team/manager_dashboard.html", {
        "post_form": post_form,
        "message_form": message_form,
        "latest_post": latest_post,  # Only the latest post is shown
        "sent_messages": sent_messages,
        "upcoming_fixtures": upcoming_fixtures,
        "fixture_availability": fixture_availability,
        "notifications": notifications,
        "posts": posts,
    })


@login_required
def add_comment(request, message_id):
    """Allows players to comment to message and notifies the manager."""
    message = get_object_or_404(ManagerMessage, id=message_id)

    if request.method == "POST":
        form = ManagerMessageCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.player = request.user
            comment.message = message
            comment.save()

            # Notify the manager who sent the message
            Notification.objects.create(
                recipient=message.manager,
                type="comment",
                message=f"{request.user.username} commented on your message.",
                link="/manager-dashboard/"
            )

            return redirect("player_dashboard")

    return redirect("player_dashboard")


@login_required
def edit_comment(request, comment_id):
    """Allows players to edit their own comments and notify the manager."""
    comment = get_object_or_404(ManagerMessageComment, id=comment_id)

    if request.user != comment.player:
        return redirect("player_dashboard")  # Prevent unauthorized access

    if request.method == "POST":
        form = ManagerMessageCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

            # Notify the manager
            Notification.objects.create(
                recipient=comment.message.manager,
                type="comment",
                message=f"{request.user.username} edited their comment on your post titled '{comment.message.title}'.",
                is_read=False,
            )

            return redirect("player_dashboard")  # Redirect back after editing
    else:
        form = ManagerMessageCommentForm(instance=comment)

    return render(request, "team/edit_comment.html", {
        "form": form, "comment": comment
    })



@login_required
def delete_comment(request, comment_id):
    """Allows players to delete their own comments."""
    comment = get_object_or_404(ManagerMessageComment, id=comment_id)

    if request.user == comment.player:
        comment.delete()

    return redirect("player_dashboard")  # Redirect back after deletion


@login_required
def mark_notification_read(request, notification_id):
    """
    Mark a specific notification as read.
    After saving, redirect the user to their correct dashboard
    based on their role or the 'next' field in the form.
    """
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

    return redirect("manager_dashboard")  # Fallback redirect


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
    """
    Allow the manager to delete a message sent to players.
    Only users with the 'manager' role are authorized to perform this action.
    """
    message = get_object_or_404(ManagerMessage, id=message_id)

    # Ensure only the manager who created the message can delete it
    if request.user.profile.role != "manager":
        return redirect("manager_dashboard")

    message.delete()
    return redirect("manager_dashboard")


@login_required
def delete_manager_post(request, post_id):
    """
    Allow a manager to delete their own post.
    Only the original manager who created the post is permitted.
    After deletion, redirect to the manager dashboard.
    """
    post = get_object_or_404(ManagerPost, id=post_id)

    # Only the manager who posted it can delete it
    if request.user != post.manager:
        return redirect("manager_dashboard")

    post.delete()  # Delete the post

    return redirect("manager_dashboard")
