from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('categories/', views.categories),
    path('questions/', views.questions),
    path('submit/', views.submit),
    path('leaderboard/', views.leaderboard),
    path('history/', views.history),
]
