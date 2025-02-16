from django import forms
from .models import (ManagerPost,
                     PlayerAvailability,
                     Profile,
                     ManagerMessage,
                     ManagerMessageComment)


class ManagerPostForm(forms.ModelForm):
    class Meta:
        model = ManagerPost
        fields = ["title", "content"]


class PlayerAvailabilityForm(forms.ModelForm):
    class Meta:
        model = PlayerAvailability
        fields = ["player", "fixture", "status"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["role"]


class ManagerMessageForm(forms.ModelForm):
    class Meta:
        model = ManagerMessage
        fields = ["title", "content"]


class ManagerMessageCommentForm(forms.ModelForm):
    class Meta:
        model = ManagerMessageComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 2, "placeholder": "Write a comment..."}),
        }