# File: mini_insta/views.py
# Author: Angelie Darbouze (angelie@bu.edu), 10/1/2025
# Description: Defines the view classes for the mini_insta app
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
from django.urls import reverse

# Create your views here.

class ProfileListView(ListView):
    """Define a view class to show all blog articles"""

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles' # note plural variable name
    ordering = ['-join_date'] # show most recent profiles first

class ProfileDetailView(DetailView):
    """Define a view class to show a single profile page"""

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile' # note singular variable name

class ProfileCreateView(CreateView): # new
    """Define a view class to create a new profile
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new profile object (POST)
    """

    model = Profile
    form_class = ProfileForm
    template_name = 'mini_insta/create_profile.html'

class PostDetailView(DetailView): #new 
    """A view class to show a single post page"""

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post' # note singular variable name

class CreatePostView(CreateView): # new 
    """ A view to handle creating a new Post on a Profile"""
    model = Post 
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self): # this is to add the profile class to the context (when you click create post for a specific profile!!)
        """Add the profile object to the context"""

        # context dictionary from the superclass
        context = super().get_context_data()
        #find and add the profile to the context
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        """This method handles the form submission and saves
        the new object to the Django database.
        We need to add the foreign key of the profile to the Comment
        object before saving it to the database.
        """
        # get the profile pk from the URL
        profile_pk = self.kwargs['pk']
        # get the Profile object associated with this pk
        profile = Profile.objects.get(pk=profile_pk)
        # associate this profile with the post being created
        form.instance.profile = profile #attach the correct profile to the post
        # Save the new Post object to the database
        post = form.save()
         # Retrieve the image_url from the POST data.
        image_url = self.request.POST.get('image_url', None)
        if image_url:
            # Create and save a Photo instance with the new Post as its foreign key.
            Photo.objects.create(post=post, image_url=image_url)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """ after successfully creating a post, return to the post detail page"""
        # get the profile pk from the URL
        pk = self.kwargs['pk']
        return reverse('show_post', kwargs={'pk': self.object.pk})