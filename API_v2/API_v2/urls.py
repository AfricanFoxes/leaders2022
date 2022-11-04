"""API_v2 URL Configuration

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
from django.urls import path
from main.views import object_api, region_api, get_all_typed_objects, predict_object_api, \
                       get_regions_objects, get_items_by_radius


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/objects/', object_api),
    path('api/predictions/', predict_object_api),
    path('api/regions/', region_api),
    path('api/objects/typed/', get_all_typed_objects),
    path('api/objects/inregion/', get_regions_objects),
    path('api/objects/byradius/', get_items_by_radius),
]
