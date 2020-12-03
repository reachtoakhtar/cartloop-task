__author__ = "akhtar"

from django.urls import path

from chat.views import ChatView, ConversationView


urlpatterns = [
    path('conversation/<str:pk>', ConversationView.as_view()),
    path('chat/', ChatView.as_view()),
]
