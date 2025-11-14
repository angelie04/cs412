# File created in class 11/11/2025 (mini_insta/serializers.py)
# Serializers convert our django data models to a 
# text-representation suitable to transmit over HTTP.

from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    """ A serializer for the profile model
    Specify  which model/fields to send to the API"""
    class Meta:
        model = Profile
        fields = ['id', 'image_url', 'caption', 'created_at']
        # fields = ['id', 'title', 'author', 'text'] for the blog example

    # add methods to customize the Create/Read/Update/Delete operartions

    def create(self, validated_data):
        """ Override the superclass method that handles object creation."""
        # profile = Profile(**validated_data)
        # profile.user = User.objects.first()  # assign to first user for now
        # profile.save()
        
        # could do the better way down below
        validated_data['user'] = User.objects.first()
        return Profile.objects.create(**validated_data)