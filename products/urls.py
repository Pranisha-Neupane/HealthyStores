from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('product/<slug:slug>/', views.detail, name='detail'),
]
