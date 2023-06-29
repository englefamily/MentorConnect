from django.urls import path
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('mentor/', api_views.mentor),
    path('student/', api_views.student),
    path('topic/', api_views.topic),
    path('feedback/', api_views.feedback),
    path('token/', api_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]