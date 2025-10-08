#mini_insta/forms.py
# Author: Angelie Darbouze (angelie@bu.edu), 10/1/2025
# Description: Defines the forms for creating and updating Profile and Post instances
from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    """Form for creating and updating Profile instances"""

    class Meta:
        model = Profile
        fields = ['username','display_name', 'bio_text', 'profile_image_url']


class CreatePostForm(forms.ModelForm):
    """Form for creating and updating Post instances"""

    class Meta:
        model = Post
        fields = ['caption'] 

class UpdateProfileForm(forms.ModelForm):
    """Form for updating Profile instances"""

    class Meta:
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']