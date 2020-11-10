"""hello_junior URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from jobs.views import JobDetailView, EmployerListView, EmployerDetailView, index


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('employers/', EmployerListView.as_view(), name='employers'),
    path('accounts/', include('accounts.urls')),
    path('job/<int:pk>', JobDetailView.as_view(), name='job_detail'),
    path('employer/<int:pk>', EmployerDetailView.as_view(), name='employer_detail'),
]

