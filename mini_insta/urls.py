# mini_insta/urls.py
# defines URL patterns for the mini_insta app
# Angelie Darbouze (angelie@bu.edu), 9/25/2025
from django.urls import path
from .views import ProfileListView, ProfileDetailView
urlpatterns = [
     path('', ProfileListView.as_view(), name='show_all_profiles'), #for the homepage
     path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'), # for the individual profile page
]

