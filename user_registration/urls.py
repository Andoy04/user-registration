from django.urls import path
from .views import Modify, RegisterView, VerifyEmail, LoginView, UserView


urlpatterns = [
    path('register/', RegisterView.as_view({'post': 'create'}), name="register"),
    path('login/', LoginView.as_view({'post': 'create'}), name="login"),
    path('verify/', VerifyEmail.as_view({'get': 'list'}), name="verify"),
    path('change-password/', Modify.as_view({'put': 'update'}), name="change-password")
]