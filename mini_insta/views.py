# mini_insta/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile 
import random
# Create your views here.

# class ShowAllView(ListView):
#     """DEfine a view class to show all blog articles"""
#     model = Profile
#     template_name = 'mini_insta/show_all.html'
#     context_object_name = 'articles'
    # ordering = ['-published']

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