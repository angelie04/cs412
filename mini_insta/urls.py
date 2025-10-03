# mini_insta/urls.py
# defines URL patterns for the mini_insta app
# Angelie Darbouze (angelie@bu.edu), 9/25/2025
from django.urls import path
from .views import *
urlpatterns = [
     path('', ProfileListView.as_view(), name='show_all_profiles'), #for the homepage
     path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'), # for the individual profile page
     path('profile/create', ProfileCreateView.as_view(), name='create_profile'), # for the create profile page
     path('profile/<int:pk>/create_comment', CommentCreateView.as_view(), name='create_comment'), # for the create comment page
     path('post/<int:pk>', PostDetailView.as_view(), name='show_post'), # for the individual post page
]

