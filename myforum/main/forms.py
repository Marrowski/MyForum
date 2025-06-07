from django import forms
from .models import UserProfile

class ChangeProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('avatar',)