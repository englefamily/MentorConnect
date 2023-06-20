from django.urls import path
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('mentor/', api_views.mentor),
    path('student/', api_views.student),
    path('topic/', api_views.topic),
    path('feedback/', api_views.feedback),
    path('token/', obtain_auth_token),
    path('register/', api_views.register, name='register'),
    path('login/', api_views.login, name='login'),
    path('resetpassword/', api_views.reset_password_request, name='reset_password_request'),
]