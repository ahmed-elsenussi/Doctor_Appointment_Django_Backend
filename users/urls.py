# writtne by [SENU]
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
# basename: to be used for the routes of the viewset
router.register(r'', UserViewSet, basename='users')
urlpatterns =router.urls