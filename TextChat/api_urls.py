from django.urls import path
from . import api_views

urlpatterns = [
    path('chat/', api_views.chat),
    path('message/', api_views.message),
]