from django.contrib import admin
from .models import PObject, Region
from leaflet.admin import LeafletGeoAdmin


admin.site.register(PObject, LeafletGeoAdmin)
admin.site.register(Region, LeafletGeoAdmin)
