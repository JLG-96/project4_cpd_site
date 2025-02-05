from django.db import models
from django.db.models import Q

class Fixture(models.Model):
    HOME_OR_AWAY = [
        ('H', 'Home'),
        ('A', 'Away'),
    ]
    opponent = models.ForeignKey("Team", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    home_or_away = models.CharField(max_length=1, choices=HOME_OR_AWAY)
    goals_for = models.PositiveIntegerField(null=True, blank=True)
    goals_against = models.PositiveIntegerField(null=True, blank=True)
    match_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.opponent.name if self.opponent else 'Unknown Team'} - {self.date} ({'Home' if self.home_or_away == 'H' else 'Away'})"


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
        """ Recalculates the team's standings based on completed fixtures. """
        print(f"\n⚽ Updating standings for {self.name}...")

        # Reset current stats
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

        # Find all completed matches where this team was involved
        completed_fixtures = Fixture.objects.filter(match_completed=True).filter(
            Q(opponent=self) | Q(home_or_away="H", opponent__isnull=False)
        )

        print(f"📌 Found {completed_fixtures.count()} completed fixtures.")

        for fixture in completed_fixtures:
            print(f"- Processing fixture: {fixture} | Goals For: {fixture.goals_for}, Goals Against: {fixture.goals_against}")

            self.games_played += 1

            # **If this team was the home team**
            if fixture.home_or_away == "H" and fixture.opponent != self:
                self.goals_for += fixture.goals_for
                self.goals_against += fixture.goals_against

                if fixture.goals_for > fixture.goals_against:  # **Win**
                    self.wins += 1
                    self.points += 3
                    print("✅ Home team won this match!")
                elif fixture.goals_for == fixture.goals_against:  # **Draw**
                    self.draws += 1
                    self.points += 1
                    print("⚠️ Match was a draw.")
                else:  # **Loss**
                    self.losses += 1
                    print("❌ Home team lost this match.")

            # **If this team was the opponent (away team)**
            elif fixture.opponent == self:
                self.goals_for += fixture.goals_against
                self.goals_against += fixture.goals_for

                if fixture.goals_against > fixture.goals_for:  # **Win**
                    self.wins += 1
                    self.points += 3
                    print("✅ Away team won this match!")
                elif fixture.goals_against == fixture.goals_for:  # **Draw**
                    self.draws += 1
                    self.points += 1
                    print("⚠️ Match was a draw.")
                else:  # **Loss**
                    self.losses += 1
                    print("❌ Away team lost this match.")

        # Save the updated stats
        print(f"🔄 Saving updated stats for {self.name}...")
        self.save()
        print(f"✅ Updated: Games Played: {self.games_played}, Wins: {self.wins}, Draws: {self.draws}, Losses: {self.losses}, Points: {self.points}")

    def __str__(self):
        return f"{self.name} - {self.points} pts"
