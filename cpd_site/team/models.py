from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Team(models.Model):
    name = models.CharField(max_length=100, default="CPD Yr Wyddgrug")
    manager = models.CharField(max_length=100)
    home_ground = models.CharField(max_length=100)
    founded_year = models.PositiveIntegerField()
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    games_played = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def calculate_standings(self):
        """Recalculate the team's standings based on completed fixtures."""
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

        completed_fixtures = Fixture.objects.filter(match_completed=True).filter(
            Q(opponent=self) | Q(home_or_away="H", opponent__isnull=False)
        )

        for fixture in completed_fixtures:
            self.games_played += 1

            if fixture.home_or_away == "H" and fixture.opponent != self:
                self.goals_for += fixture.goals_for
                self.goals_against += fixture.goals_against
                if fixture.goals_for > fixture.goals_against:
                    self.wins += 1
                    self.points += 3
                elif fixture.goals_for == fixture.goals_against:
                    self.draws += 1
                    self.points += 1
                else:
                    self.losses += 1

            elif fixture.opponent == self:
                self.goals_for += fixture.goals_against
                self.goals_against += fixture.goals_for
                if fixture.goals_against > fixture.goals_for:
                    self.wins += 1
                    self.points += 3
                elif fixture.goals_against == fixture.goals_for:
                    self.draws += 1
                    self.points += 1
                else:
                    self.losses += 1

        self.save()

    def __str__(self):
        return f"{self.name} - {self.points} pts"


class Fixture(models.Model):
    HOME_OR_AWAY = [
        ('H', 'Home'),
        ('A', 'Away'),
    ]
    opponent = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    home_or_away = models.CharField(max_length=1, choices=HOME_OR_AWAY)
    goals_for = models.PositiveIntegerField(null=True, blank=True)
    goals_against = models.PositiveIntegerField(null=True, blank=True)
    match_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.opponent.name if self.opponent else 'Unknown Team'} - {self.date} ({'Home' if self.home_or_away == 'H' else 'Away'})"


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.team.name if self.team else 'No Team'}"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('player', 'Player'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class ManagerPost(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PlayerAvailability(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    fixture = models.ForeignKey(Fixture, on_delete=models.CASCADE)
    available = models.BooleanField()

    def __str__(self):
        return f"{self.player.username} - {
            'Available' if self.available else 'Unavailable'}"
