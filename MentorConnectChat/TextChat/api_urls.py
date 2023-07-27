from django.urls import path
from . import api_views

urlpatterns = [
    path('chat/', api_views.chat),
    path('message/', api_views.message),
    path('get-chats/<str:user_id>/', api_views.get_chats),
    path('get-messages/<str:chat_id>/', api_views.get_messages)
]