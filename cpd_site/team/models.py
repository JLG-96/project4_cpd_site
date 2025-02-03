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
        return self.name