# File: restaurant/urls.py
# Author: Angelie Darbouze (angelie@bu.edu)
# Description: url patterms for the 'restaurant' app

from django.urls import path
from django.conf import settings
from . import views

# url patterns for the restaurant app
urlpatterns = [
    path('', views.home, name='home'),
    path("order/", views.order_form, name='order_form'),
    path ("submit/", views.submit, name='submit'),
]