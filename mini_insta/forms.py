#mini_insta/forms.py
from django import forms
from .models import Profile, Comment

class ProfileForm(forms.ModelForm):
    """Form for creating and updating Profile instances"""

    class Meta:
        model = Profile
        fields = ['username','display_name', 'bio_text', 'profile_image_url']

class CommentForm(forms.ModelForm): # in my case this is a post and it has to link to
    """Form for creating and updating Comment instances"""

    class Meta:
        model = Comment
        fields = [ 'author', 'text']

## make one for post too 