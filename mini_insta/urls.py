# mini_insta/urls.py
# defines URL patterns for the mini_insta app
# Angelie Darbouze (angelie@bu.edu), 10/1/2025
from django.urls import path
from .views import *
urlpatterns = [
     path('', ProfileListView.as_view(), name='show_all_profiles'), #for the homepage
     path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'), # for the individual profile page
     path('profile/create', ProfileCreateView.as_view(), name='create_profile'), # for the create profile page
     path('post/<int:pk>', PostDetailView.as_view(), name='show_post'), # for the individual post page
     path('profile/<int:pk>/create_post/', CreatePostView.as_view(), name='create_post'), # for the create post page
     path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'), # for the update profile page
     path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'), # for the delete post page
     path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'), # for the update post page
     path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'), # for the show followers page
     path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'), # for the show following page
     path('profile/<int:pk>/feed', PostFeedListView.as_view(), name = 'show_feed' ), # for the show feed page
]