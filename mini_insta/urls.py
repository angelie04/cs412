#mini_insta/urls.py
from django.urls import path
from .views import ProfileListView
urlpatterns = [
    # path('', RandomArticleView.as_view(), name='random'),
     path('', ProfileListView.as_view(), name='show_all_profiles'), # modified
    # path('article/<int:pk>',ArticleView.as_view(), name = 'article')
]

