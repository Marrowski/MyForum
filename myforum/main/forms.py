from django import forms
from .models import UserProfile, Comment

class ChangeProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('avatar',)
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)