#project/forms.py
# Author: Angelie Darbouze (angelie@bu.edu), 12/3/2025
# Description: Defines the forms for creating and updating Restaurant and Review instances
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RestaurantForm(forms.ModelForm):
    """Form for creating and updating Restaurant instances"""

    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'categories', 'website', 'image']    

class ReviewForm(forms.ModelForm):
    """Form for creating and updating Review instances"""

    class Meta:
        model = Review
        fields = ['rating', 'comment']

class SignUpForm(UserCreationForm):
    display_name = forms.CharField(max_length=150, required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "display_name", "password1", "password2", "profile_image")

    def save(self, commit=True):
        user = super().save(commit=commit)  # creates the User
        # create/update the Profile linked to this user
        Profile.objects.update_or_create(
            revize_user=user,
            defaults={
                "username": user.username,
                "display_name": self.cleaned_data.get("display_name") or user.username,
                "profile_image": self.cleaned_data.get("profile_image"),
            },
        )
        return user