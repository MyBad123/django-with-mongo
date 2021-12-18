from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    register,
    auth, 
)

urlpatterns = [
    path('access/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    
    #api for reg and auth
    path('reg/', register),
    path('auth/', auth),
]
