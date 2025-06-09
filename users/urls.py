# writtne by [SENU]
from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet,
    CurrentUserView,
    verify_email,
    google_authenticate,
    GoogleLogin,
    CustomTokenObtainPairView
)
router = DefaultRouter()
# basename: to be used for the routes of the viewset
router.register(r'', UserViewSet, basename='users')
urlpatterns =[
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<str:token>/', verify_email, name='verify-email'),
    path('google-auth/', google_authenticate, name='google-auth'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
]
urlpatterns += router.urls