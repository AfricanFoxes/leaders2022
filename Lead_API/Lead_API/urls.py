"""Lead_API URL Configuration

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
from django.urls import path, re_path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/objects', get_all_objects, name="objects"),
    path('api/object', get_object, name="object"),
    path('api/regions', get_all_regions, name="regions"),
    path('api/region', get_region, name="region"),
    path('api/predictions', get_all_predictions, name="predictions"),
    path('api/objects/typed', get_all_typed_objects, name="typed"),
    path('api/objects/region', get_objects_for_region, name="objectregions"),
]
