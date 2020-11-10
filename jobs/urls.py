from django.urls import path
from . import views

urlpatterns = [
    path('', views.jobs_list, name='jobs'),
]