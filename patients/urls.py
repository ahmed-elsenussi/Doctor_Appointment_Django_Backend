# written by [SENU]
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet

router = DefaultRouter()
# basename to be used in viewset routes
router.register(r'', PatientViewSet, basename='patients')
urlpatterns = router.urls