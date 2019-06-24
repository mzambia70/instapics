from django import forms
from .models import *

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['main_user', 'profile', 'upload_date', 'likes', 'comments']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude=['main_user','picture', 'upload_date']

class LikeForm(forms.ModelForm):
    class Meta:
        model=Like
        exclude=['main_user','picture']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['main_user', 'followers', 'following']

class FollowForm(forms.ModelForm):
    class Meta:
        model=Contact
        exclude=['user_from','user_to','created']