# File: mini_insta/views.py
# Author: Angelie Darbouze (angelie@bu.edu), 9/25/2025
# Description: Defines the view classes for the mini_insta app
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile 

# Create your views here.

class ProfileListView(ListView):
    """Define a view class to show all blog articles"""

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles' # note plural variable name
    ordering = ['-join_date'] # show most recent profiles first

class ProfileDetailView(DetailView):
    """Define a view class to show a single profile page"""

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile' # note singular variable name
