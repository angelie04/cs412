# Serializers convert our django data models to a 
# text-representation suitable to transmit over HTTP.
# seralizers.py
# Angelie Darbouze (angelie@bu.edu)
from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    """ A serializer for the Joke model"""
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    """ A serializer for the Picture model"""
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created_at']
