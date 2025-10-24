# mini_insta/urls.py
# defines URL patterns for the mini_insta app
# Angelie Darbouze (angelie@bu.edu), 10/1/2025
from django.urls import path
from .views import *
#generic view for authentication/authorization
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', ProfileListView.as_view(), name='show_all_profiles'), #for the homepage
     path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'), # for the individual profile page
     path('profile/create_profile', CreateProfileView.as_view(), name='create_profile'), # for the create profile page
     path('post/<int:pk>', PostDetailView.as_view(), name='show_post'), # for the individual post page
     path('profile/create_post', CreatePostView.as_view(), name='create_post'), # for the create post page
     path('profile/update', UpdateProfileView.as_view(), name='update_profile'), # for the update profile page
     path('post/delete', DeletePostView.as_view(), name='delete_post'), # for the delete post page
     path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'), # for the update post page
     path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'), # for the show followers page
     path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'), # for the show following page
     path('profile/feed', PostFeedListView.as_view(), name='show_feed' ), # for the show feed page
     path('profile/search', SearchView.as_view(), name='search_results'), # for the search posts page
     ## authorization URLS
     path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
     # path('register/', UserRegistrationView.as_view(), name='register'), # new user registration
     path('logout_confirmation/', UserLogoutView.as_view(), name='logout_confirmation'),
     #task 4 assignment 7 URLs
     path('profile/<int:pk>/follow', FollowProfileView.as_view(), name='follow_profile'), # to follow a profile
     path('profile/<int:pk>/delete_follow', DeleteFollowProfileView.as_view(), name='unfollow_profile'), # to unfollow a profile
     path('post/<int:pk>/like', LikePostView.as_view(), name='like_post'), # to like a post
     path('post/<int:pk>/delete_like', DeleteLikePostView.as_view(), name='unlike_post'), # to unlike a post
]