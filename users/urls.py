# writtne by [SENU]
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, verify_email, google_authenticate,GoogleLogin,CustomTokenObtainPairView

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
# basename: to be used for the routes of the viewset
router.register(r'', UserViewSet, basename='users')
urlpatterns =[
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<str:token>/', verify_email, name='verify-email'),
    path('google-auth/', google_authenticate, name='google-auth'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
]+router.urls