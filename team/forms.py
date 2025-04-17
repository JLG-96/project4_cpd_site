from django import forms
from .models import (ManagerPost,
                     PlayerAvailability,
                     Profile,
                     ManagerMessage,
                     ManagerMessageComment)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ManagerPostForm(forms.ModelForm):
    """
    Form for managers to create or edit a post
    containing match announcements or commentary.
    """
    class Meta:
        model = ManagerPost
        fields = ["title", "content"]


class PlayerAvailabilityForm(forms.ModelForm):
    """
    Form for players to set their availability status
    for a specific fixture.
    """
    class Meta:
        model = PlayerAvailability
        fields = ["player", "fixture", "status"]


class ProfileForm(forms.ModelForm):
    """
    Form to allow editing the user's role
    (player or manager) in their profile.
    """
    class Meta:
        model = Profile
        fields = ["role"]


class ManagerMessageForm(forms.ModelForm):
    """
    Form for managers to compose messages to players.
    """
    class Meta:
        model = ManagerMessage
        fields = ["title", "content"]


class ManagerMessageCommentForm(forms.ModelForm):
    """
    Form for players to comment on a manager's message.
    Includes a styled textarea widget for UX.
    """
    class Meta:
        model = ManagerMessageComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 2, "placeholder": "Write a comment..."}),
        }


class CustomUserRegistrationForm(UserCreationForm):
    """
    Custom user registration form with role selection
    and an invite code for security.
    """
    ROLE_CHOICES = [
        ("player", "Player"),
        ("manager", "Manager"),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    invite_code = forms.CharField(
        max_length=100,
        help_text="Enter the invite code provided by the club."
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_invite_code(self):
        code = self.cleaned_data["invite_code"]
        if code != "wyddgrug2024":
            raise ValidationError("Invalid invite code.")
        return code
