from posixpath import basename
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from user_registration.views import UserView

router = routers.DefaultRouter()
router.register(f'list', UserView, basename='list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_registration.urls')),
    path('user/', include(router.urls))
]