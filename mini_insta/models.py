# mini_insta/models.py
# define data models for the blog application
from django.db import models

# Create your models here.
#created from modules in blackboard
# class Article(models.Model):
#     #define fields for the Article model
#     """ Encapsulatres the data of a blog Article by an author"""
#     title = models.TextField(blank = True)
#     author = models.TextField(blank=True)
#     text = models.TextField(blank=True)
#     published = models.DateTimeField(auto_now=True)
#     image_url = models.URLField(blank=True)
    
#     def __str__(self):
#          """ return a string representation of the Article model"""
#          return self.title

class Profile(models.Model):
    """Models the data attributes of an individual user profile"""
    #define data attributes of a user profile
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
         """ return a string representation of the Profile model"""
         return self.display_name