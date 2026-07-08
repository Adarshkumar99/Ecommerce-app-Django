from django.urls import path, include
from . import views

# Root-level routes: home, contact and about pages.
urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
