# File: mini_insta/models.py
# Author: Angelie Darbouze (angelie@bu.edu), 10/1/2025
# Description: Defines data models for the mini_insta application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
class Profile(models.Model):
    """Models the data attributes of an individual user profile"""
    # define data attributes of a user profile
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """ return a string representation of the Profile model"""
        return self.display_name

    def get_absolute_url(self): 
        """ returns the URL to access a particular profile instance"""
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_all_posts(self):
        """return a queryset of posts about this profile"""
        # use object manager to retrieve posts about this profile
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_post_count(self):
        """ count the number of posts on this profile"""
        return self.get_all_posts().count()
    
    def get_followers(self):
        """ returns a list of those Profiles who are followers of this Profile.
        (subscribers who will see Posts from this profile)"""
        follows = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in follows]
    
    def get_num_followers(self):
        """return the count of followers"""
        count = len(self.get_followers())
        return count

    def get_following(self):
        """Returns the list of those Profiles followed by this profile."""
        follows = Follow.objects.filter(follower_profile=self)
        return [follow.profile for follow in follows]

    def get_num_following(self):
        """Return the count of how many profiles are being followeed"""
        count = len(self.get_following())
        return count
    
    def get_post_feed(self):
        """returns a list of Posts, specifically for the profiles being 
        followed by the profiles on which the method was called """
        # profile = Profile.objects.get(pk=self.pk)
        following_profile = self.get_following()
        return Post.objects.filter(profile__in=following_profile)
    
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
    
    def get_all_comments(self):
        """get all comments for this post"""
        comments = Comment.objects.filter(post=self)
        return comments

    def get_likes(self):
        """get all likes for this post"""
        likes = Like.objects.filter(post=self)
        return likes

class Photo (models.Model):
    """ models the data attributes of a photo in a post"""

    #data attributes for a photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=False)

    def __str__(self):
        """ return a string representation of the Photo model  
        using image_file if available, otherwise image_url."""
        return self.get_image_url()

    def get_image_url(self):
        """ return the URL to the image"""
        if self.image_file:
            return self.image_file.url
        return self.image_url
    
class Follow(models.Model): # new model
    """ encapsulates the idea of an edge connecting two nodes with the social network.
    (Basically when one Profile follows another Profile)"""

    #data attributes for Follow relation
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name="profile") # reverse accessor for the creater side
    follower_profile = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = "follower_profile") # reverse accessor for the subscriber side
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Allows me to view this Follow relationship as a string representation"""
        return f'{self.follower_profile} follows {self.profile}'
    

class Comment(models.Model):
    """encapsulates the idea of one Profile providing a response or commentary on a Post """

    #data attributes
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        """return string representation for Comment model"""
        return f'Comment by {self.profile} on {self.post}: {self.text}'
    
class Like(models.Model):
    """encapsulates the idea of one Profile providing approval of a Post"""

    #data attributes
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """return string representation for Like model"""
        return f'Liked by {self.profile}'