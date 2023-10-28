from django import forms
from .models import ChatterProfile

class ChatterProfileForm(forms.ModelForm):
    class Meta:
        model = ChatterProfile
        fields = {'avatar',}