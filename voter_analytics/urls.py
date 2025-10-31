# voter_analytics/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.VoterListView.as_view(), name="home"),
    path("voters/", views.VoterListView.as_view(), name="voter_list"),
    path("voters/<int:pk>/", views.VoterDetailView.as_view(), name="voter_detail"),
    path("graphs/", views.VoterGraphView.as_view(), name="graphs"),
]