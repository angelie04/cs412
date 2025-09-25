# mini_insta/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile 
import random
# Create your views here.

class ProfileListView(ListView):
    """Define a view class to show all blog articles"""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles' # note plural variable name
    ordering = ['-join_date'] # show most recent articles first

# class ArticleView(DetailView):
#     """Define a view class to show a single blog article"""
#     model = Article
#     template_name = 'mini_insta/article.html'
#     context_object_name = 'article' # note singular variable name

# class RandomArticleView(DetailView):
#     """Define a view class to show a random blog article"""
#     model = Article
#     template_name = 'mini_insta/article.html'
#     context_object_name = 'article' # note singular variable name
#     # methods
#     def get_object(self):
#         """ return a random Article object from the database"""
#         all_articles = Article.objects.all()
#         return random.choice(all_articles)