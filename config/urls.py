#  written by [SENU]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # [SENU] handle view image
from django.conf.urls.static import static # [SENU] handle view image

urlpatterns = [

    path('admin/', admin.site.urls),

    # other apps urls 
    path('users/', include('users.urls') ),
    path('doctors/', include('doctors.urls')), # for doctors and the specializations
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('notifications/', include('notifications.urls')),
    # [AMS] for using JWT authentication and google login
    path('auth/', include('social_django.urls', namespace='social')),
]



# [SENU] handle view image
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)