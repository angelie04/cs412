# File: mini_insta/models.py
# Author: Angelie Darbouze (angelie@bu.edu), 9/25/2025
# Description: Defines data models for the mini_insta application
from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self): #might not need this
        """ returns the URL to access a particular profile instance"""
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_all_posts(self):
        """return a queryset of posts about this profile"""
        # use object manager to retrieve posts about this profile
        posts = Post.objects.filter(profile=self)
        return posts

class Comment(models.Model):
    """ models the data attributes of a comment on a profile"""

    #data attributes for a comment
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    author = models.TextField(blank=False)

    def __str__(self):
        """ return a string representation of the Comment model"""
        return f' {self.text}' 
    
class Post(models.Model):
    """ models the data attributes of a post on a profile"""

    #data attributes for a post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=False)

    def __str__(self):
        """ return a string representation of the Post model"""
        return f' {self.caption}'
    
    def get_all_photos(self):
        """ return a queryset of photos about this post"""
        # use object manager to retrieve photos about this post
        photos = Photo.objects.filter(post=self)
        return photos
    
class Photo (models.Model):
    """ models the data attributes of a photo in a post"""

    #data attributes for a photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ return a string representation of the Photo model"""
        return f' {self.image_url}'
    
