from django.urls import path
from .views import UserRegister, UserLogin, UserLogout, verify_email

urlpatterns = [
  path('register/', UserRegister, name='register'),
  path('login/', UserLogin, name='login'),
  path('logout/', UserLogout, name='logout'),
  path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
]