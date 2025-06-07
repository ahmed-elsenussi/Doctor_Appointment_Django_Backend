#  written by [SENU]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    # other apps urls 
    path('users/', include('users.urls') ),
    path('doctors/', include('doctors.urls')), # for doctors and the specializations
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('notifications/', include('notifications.urls')),

]
