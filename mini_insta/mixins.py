# mini_insta/mixins.py
# was created to hold custom mixins for the mini_insta app
#Angelie Darbouze (angelie@bu.edu), 10/22/2025
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Profile

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    """Custom mixin to require login and provide the current profile automatically."""
    login_url = 'login'  

    def get_logged_in_profile(self):
        # Retrieve the profile from the URL's pk.
        return get_object_or_404(Profile, pk=self.kwargs.get('pk'))
    def get_login_url(self):
        # Return the URL to your app's login page
        return reverse('login')