from django.contrib import admin
from django.urls import path

from . import views
from .views import BlackjackGame

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),

    path('api/blackjack/', BlackjackGame.as_view())
]
