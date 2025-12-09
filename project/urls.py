# File: urls.py
# Author: Angelie Darbouze (angelie@bu.edu), 11/25/2025
# Description: Defines the URL patterns for the project app 

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant_list'),
    path('review/', ReviewView.as_view(), name='review'),
    path('restaurants/<int:restaurant_id>/review', WriteReview.as_view(), name='write_review'),
    ## authorization URLS
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile_detail'), # for the individual profile page
    path('profile/update', UpdateProfileView.as_view(), name='profile_edit'), # for the update profile page
    path('search/', RestaurantSearchView.as_view(), name='search_results'), # for restaurant search
    path('review/success/', ReviewSuccessView.as_view(), name='success_review'), # review success page
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'), # restaurant detail page
]