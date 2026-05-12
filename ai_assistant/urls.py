from django.urls import path
from .views import chat_endpoint

urlpatterns = [
    path('chat/', chat_endpoint, name='ai_chat'),
]