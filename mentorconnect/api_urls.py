from django.urls import path
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('mentor/', api_views.mentor),
    path('student/', api_views.student),
    path('topic/', api_views.topic),
    path('sub-topic/', api_views.sub_topic),
    path('feedback/', api_views.feedback),
    path('token/', obtain_auth_token),
]