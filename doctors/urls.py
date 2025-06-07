# written by [SENU]
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, SpecializatoinViewSet

router = DefaultRouter()

# Register doctors under explicit path "list"
router.register(r'doctors', DoctorViewSet, basename='doctors')

# Register specializations at /doctors/specializations/
router.register(r'specializations', SpecializatoinViewSet, basename='specializations')

urlpatterns = router.urls
