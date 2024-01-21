from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tester.urls')),
    path('smart-selects/', include('smart_selects.urls')),
]
