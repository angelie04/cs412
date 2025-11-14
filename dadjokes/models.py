from django.db import models

# Create your models here.

class Joke(models.Model):
    """Model to store the text of a joke"""
    text = models.TextField()
    contributor = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Joke model"""
        return f"{self.text} - {self.contributor}"
    
class Picture(models.Model):
    """Model to store a image_url """
    image_url = models.URLField(max_length=1000)
    contributor = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Picture model"""
        return self.image_url
    
