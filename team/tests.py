from django.test import TestCase
from django.urls import reverse
from .models import Team
# Create your tests here.


class TeamModelTest(TestCase):
    def setUp(self):
        # Create a sample team
        self.team = Team.objects.create(
            name="Brymbo FC",
            logo="brymbo_logo.jpg",
        )

    def test_team_str(self):
        # Test the string representation of a team
        self.assertEqual(str(self.team), "Brymbo FC")


class HomePageViewTest(TestCase):
    def setUp(self):
        # Set up a sample team for fixtures, etc.
        Team.objects.create(
            name="Rhydymwyn FC",
            logo="rhyd_logo.jpg",
        )

    def test_homepage_status_code(self):
        # Ensure that the homepage loads successfully
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'team/home.html')
