from django.urls import path
from . import views

app_name = 'feedbacks'

urlpatterns = [
    path('', views.feedback, name='feedback'),
]
