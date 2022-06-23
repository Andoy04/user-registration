from django.contrib import admin
from django.urls import path, include
from user_registration.views import UserViewSet
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'user', UserViewSet) #the route tha will be used to access your API on the browser


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
