# File: mini_insta/views.py
# Author: Angelie Darbouze (angelie@bu.edu), 10/1/2025
# Description: Defines the view classes for the mini_insta app
from multiprocessing import context
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .forms import *
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin ## for authentication
from django.contrib.auth.forms import UserCreationForm ## for new User
from django.contrib.auth.models import User ## the Django user model
from .mixins import ProfileLoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth import login

# Create your views here.

class ProfileListView(ListView):
    """Define a view class to show all blog articles"""

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles' # note plural variable name
    ordering = ['-join_date'] # show most recent profiles first

    def dispatch (self, request, *args, **kwargs): #new from video
        """Override dispatch to add the current profile to the context."""
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user).first()
            if profile:
                return redirect('show_profile', pk=profile.pk)
        return super().dispatch(request, *args, **kwargs)
    
class ProfileDetailView(DetailView):
    """Define a view class to show a single profile page"""

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile' # note singular variable name

# class ProfileCreateView(CreateView): # new
#     """Define a view class to create a new profile
#     (1) display the HTML form to user (GET)
#     (2) process the form submission and store the new profile object (POST)
#     """

#     model = Profile
#     form_class = ProfileForm
#     template_name = 'mini_insta/create_profile.html'

class PostDetailView(DetailView): #new 
    """A view class to show a single post page"""

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post' # note singular variable name

class CreatePostView(ProfileLoginRequiredMixin, CreateView): 
    """ A view to handle creating a new Post on a Profile"""
    model = Post 
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_login_url(self):
        """Return the login URL to redirect to if the user is not authenticated."""
        return reverse('login')

    def get_context_data(self): # this is to add the profile class to the context (when you click create post for a specific profile!!)
        """Add the profile object to the context"""

        # context dictionary from the superclass
        context = super().get_context_data()
        #updated so that it gets the logged in user's profile
        current_profile = Profile.objects.get(user=self.request.user)
        context['profile'] = current_profile
        return context
    
    def form_valid(self, form):
        """Attach the logged-in user's profile to the new Post and save."""
        current_profile = Profile.objects.filter(user=self.request.user).first()
        if not current_profile:
            # either redirect to profile creation or raise an error
            return redirect('create_profile')
        form.instance.profile = current_profile
        post = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=post, image_file=file)

        # attach the user to the profile instance (optional)
        form.instance.profile.user = self.request.user

        return super().form_valid(form)
    
    def get_success_url(self):
        """ after successfully creating a post, return to the post detail page"""
        # get the profile pk from the URL
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
class UpdateProfileView(ProfileLoginRequiredMixin, UpdateView): # new
    """This view class updates an existing profile
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the updated profile object (POST)
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        # Return the Profile associated with the logged-in user.
        return Profile.objects.filter(user=self.request.user).first()

class DeletePostView(ProfileLoginRequiredMixin, DeleteView):
    """This view class deletes an existing post
    (1) display the HTML form to user (GET)
    (2) process the form submission and delete the post object (POST)
    """
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        """Add the post and its profile to the context."""
        
        context = super().get_context_data(**kwargs)
        post = self.get_object()  # the post to be deleted
        context['post'] = post
        context['profile'] = post.profile
        return context
    
    def get_success_url(self):
        """ after successfully deleting a post, return to the profile detail page"""
    
        pk = self.kwargs['pk']  #find pk for this post 
        post = Post.objects.get(pk=pk) #find the post object
        profile_pk = post.profile.pk  # get the profile pk from the post object
        return reverse('show_profile', kwargs={'pk': profile_pk})

class UpdatePostView(ProfileLoginRequiredMixin, UpdateView):
    """This view class updates an existing post
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the updated post object (POST)
    """
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_context_data(self, **kwargs):
        """Add the post to the context."""

        context = super().get_context_data(**kwargs)
        post = self.get_object()  
        context['post'] = post
        return context
    
    def get_success_url(self):
        """ after successfully updating a post, return to the post detail page"""

        pk = self.kwargs['pk']  #find pk for this post 
        return reverse('show_post', kwargs={'pk': pk})
    
class ShowFollowersDetailView(DetailView):
    """ A view class to show a list of followers for a profile"""
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile' # note singular variable name

class ShowFollowingDetailView(DetailView):
    """ A view class to show a list of profiles that a profile is following"""
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile' # note singular variable name

class PostFeedListView(ProfileLoginRequiredMixin, ListView):
    """A view class to show a users feed list"""

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'
    

    def get_queryset(self):
        """Filter to return only the Profile for the given pk from the URL.""" 

        # return Profile.objects.filter(pk=self.kwargs['pk'])
        current_profile = Profile.objects.filter(user=self.request.user).first()
        return current_profile.get_post_feed() 

    def get_context_data(self, **kwargs):
        """Add the post feed to the context."""

        context = super().get_context_data(**kwargs)
        #updated so that it gets the logged in user's profile
        current_profile = Profile.objects.filter(user=self.request.user).first()
        context['profile'] = current_profile
        return context
    
class SearchView(ProfileLoginRequiredMixin, ListView):
    """A view class for searching profiles"""

    model = Profile
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'profiles'  

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to check for the presence of the query parameter."""

        # Use the pk from the URL instead of the session
        current_profile = Profile.objects.filter(user=self.request.user).first()
        if not request.GET.get('query'):
            # If there is no query, render the search form with the current profile in context.
            return render(request, 'mini_insta/search.html', {'profile': current_profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Filter posts based on the search query."""

        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        """Add additional context data for the search results page."""

        context = super().get_context_data(**kwargs)
        #updated so that it gets the logged in user's profile
        current_profile = Profile.objects.filter(user=self.request.user).first()
        query = self.request.GET.get('query', '')
        # Get posts matching the query (similar to get_queryset)
        posts = Post.objects.filter(caption__icontains=query)

        # Get profiles matching the query in username, display_name, or bio_text
        # imported Q from django.db.models for this
        matching_profiles = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )
        context['profile'] = current_profile
        context['query'] = query
        context['posts'] = posts
        context['profiles'] = matching_profiles
        return context
    
class UserLogoutView(TemplateView):
    """ A view class to handle user logout"""
    template_name = 'mini_insta/logged_out.html'

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self,**kwargs):
        """Add the profile object to the context"""
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()  # Add the UserCreationForm instance
        return context

    def form_valid(self, form):
        """This method handles the form submission and saves
        the new object to the Django database.
        We need to add the foreign key of the profile to the Comment
        object before saving it to the database.
        """
        # Reconstruct the UserCreationForm instance from the self.request.POST data
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user # Attach the Django User to the Profile instance object
            return super().form_valid(form) # Delegate the rest to the super class
        else:
            # If user_form is not valid, re-render the form
            return self.form_invalid(form)
        
class FollowProfileView(ProfileLoginRequiredMixin, TemplateView):
    """ A view class to handle following a profile"""
    template_name = 'mini_insta/follow_profile.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the profile to follow (from URL)
        target_profile = Profile.objects.get(pk=self.kwargs['pk'])
        # Get the logged-in user's profile
        follower_profile = Profile.objects.filter(user=request.user).first()
        # Prevent following self
        if follower_profile != target_profile:
            Follow.objects.get_or_create(profile=target_profile, follower_profile=follower_profile)
        # Redirect to the target profile page
        return redirect('show_profile', pk=target_profile.pk)
    
class DeleteFollowProfileView(ProfileLoginRequiredMixin, TemplateView):
    template_name = 'mini_insta/unfollow_profile.html'

    def dispatch(self, request, *args, **kwargs):
        target_profile = Profile.objects.get(pk=self.kwargs['pk'])
        follower_profile = Profile.objects.filter(user=request.user).first()
        # Prevent unfollowing self (optional, but safe)
        if follower_profile != target_profile:
            Follow.objects.filter(profile=target_profile, follower_profile=follower_profile).delete()
        return redirect('show_profile', pk=target_profile.pk)
    
class LikePostView(ProfileLoginRequiredMixin, TemplateView):
    template_name = 'mini_insta/like_post.html'

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        liker_profile = Profile.objects.filter(user=request.user).first()
        # Prevent liking own post
        if post.profile != liker_profile:
            Like.objects.get_or_create(post=post, profile=liker_profile)
        return redirect('show_post', pk=post.pk)
    
class DeleteLikePostView(ProfileLoginRequiredMixin, TemplateView):
    template_name = 'mini_insta/unlike_post.html'

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        liker_profile = Profile.objects.filter(user=request.user).first()
        # Prevent unliking own post (optional)
        if post.profile != liker_profile:
            Like.objects.filter(post=post, profile=liker_profile).delete()
        return redirect('show_post', pk=post.pk)
    

#############################################################
# created in class 11/11/2025
# REST API:

from rest_framework import generics
from .serializers import *

class ProfileAPIView(generics.ListCreateAPIView):
    """ An API view to return a listing of profiles and to create a profile"""
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer