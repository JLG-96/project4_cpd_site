from django import forms
from .models import ManagerPost, PlayerAvailability, Profile


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