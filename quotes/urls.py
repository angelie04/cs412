from django.urls import path
#from django.config import settings
from .views import main_page, about_page,show_all

urlpatterns = [
    path("", main_page,name = "main_page"),
    path("about", about_page, name = "about_page"),
    path("show_all", show_all, name = "all_quotes" ),
]