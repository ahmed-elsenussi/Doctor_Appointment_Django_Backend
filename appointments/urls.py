# [SENU]: simialr to simple router but contain root api view
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet

router = DefaultRouter()

# [SENU]: based name to be used by the DRF: appointments-list, apponitments-details...etc
router.register(r'', AppointmentViewSet, basename='appointments')
urlpatterns = router.urls
