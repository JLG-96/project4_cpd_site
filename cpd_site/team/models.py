from django.db import models

# Create your models here.
class Team(models.Model):
    # Core team information (focused on CPD Yr Wyddgrug)
    name = models.CharField(max_length=100, default="CPD Yr Wyddgrug")  # Pre-filled for CPD Yr Wyddgrug
    manager = models.CharField(max_length=100)  # Manager's name
    home_ground = models.CharField(max_length=100)  # Home ground name
    founded_year = models.PositiveIntegerField()  # Year the team was founded
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)  # Club logo

    # Team stats for league tracking
    games_played = models.PositiveIntegerField(default=0)  # Total games played
    wins = models.PositiveIntegerField(default=0)  # Number of wins
    draws = models.PositiveIntegerField(default=0)  # Number of draws
    losses = models.PositiveIntegerField(default=0)  # Number of losses
    goals_for = models.PositiveIntegerField(default=0)  # Total goals scored
    goals_against = models.PositiveIntegerField(default=0)  # Total goals conceded
    points = models.PositiveIntegerField(default=0)  # Total points in the league

    def __str__(self):
        return self.name  # This ensures a readable name in the admin panel


class Fixture(models.Model):
    HOME_OR_AWAY = [
        ('H', 'Home'),
        ('A', 'Away'),
    ]
    opponent = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True) # Now links to a Team
    date = models.DateField()  # Match date
    time = models.TimeField()  # Kickoff time
    location = models.CharField(max_length=100)  # Match venue
    home_or_away = models.CharField(max_length=1, choices=HOME_OR_AWAY)  # Home/Away status
    goals_for = models.PositiveIntegerField(null=True, blank=True)  # Goals scored by CPD Yr Wyddgrug
    goals_against = models.PositiveIntegerField(null=True, blank=True)  # Goals conceded
    match_completed = models.BooleanField(default=False)  # Mark if the match has been played

    def __str__(self):
        return f"{self.opponent.name if self.opponent else 'Unknown Team'} - {self.date} ({'Home' if self.home_or_away == 'H' else 'Away'})"
