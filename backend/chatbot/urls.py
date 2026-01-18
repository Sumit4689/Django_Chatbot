from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('clear-history/', views.clear_history, name='clear_history'),
    path('ingest/', views.ingest, name='ingest'),
    path('health/', views.health, name='health'),
]
