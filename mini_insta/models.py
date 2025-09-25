# File: mini_insta/models.py
# Author: Angelie Darbouze (angelie@bu.edu), 9/25/2025
# Description: Defines data models for the mini_insta application
from django.db import models

class Profile(models.Model):
    """Models the data attributes of an individual user profile"""
    # define data attributes of a user profile
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ return a string representation of the Profile model"""
        return self.display_name