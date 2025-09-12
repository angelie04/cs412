# File: urls.py
# Author: Angelie Darbouze (angelie@bu.edu), 9/12/2025
# Description: This file defines the URL patterns for the 'quotes' application. 
# It maps URL paths to their corresponding view functions, enabling navigation to the main page, about page, and the page displaying all quotes and images.
from django.urls import path
from .views import main_page, about_page,show_all

urlpatterns = [
    path("", main_page, name = "main_page"),
    path("about", about_page, name = "about_page"),
    path("show_all", show_all, name = "all_quotes" ),
]
