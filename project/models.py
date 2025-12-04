from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.

# Might remove Profile model later if not necessary
class Profile(models.Model):
    """Models the data attributes of a user profile"""
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    # changed this to a OneToOneField since mini_insta already has a ForeignKey to User
    revize_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='revize_profile')

    def __str__(self):
        """ return a string representation of the Profile model"""
        return self.display_name

class Restaurant(models.Model):
    """Model to store restaurant info"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    # phone_number = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    # add only if you want to keep a primary cuisine type for quick search... 
    # cuisine_type = models.CharField(max_length=100, blank=True)
    categories = models.ManyToManyField('Category', related_name='restaurants', blank=True)
    image = models.ImageField(upload_to="restaurants/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Restaurant model"""
        return self.name
    
    class Meta:
        ordering = ["name"]

class Review(models.Model):
    """ Stores reviews for restaurants """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 (worst) to 5 (best)")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Review model"""
        return f"Review of {self.restaurant.name} by {self.user.username} - Rating: {self.rating}"
    
class Review_images(models.Model):
    """ Model to store images associated with reviews """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="review_images/")

    def __str__(self):
        """Return a string representation of the Review_images model"""
        return f"Image for review {self.review.id} of {self.review.restaurant.name}"
    
class Category(models.Model):
    """ Model to store restaurant categories """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Return a string representation of the Category model"""
        return self.name