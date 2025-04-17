from django import forms
from .models import (ManagerPost,
                     PlayerAvailability,
                     Profile,
                     ManagerMessage,
                     ManagerMessageComment)


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