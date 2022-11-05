from django.contrib import admin
from .models import PObject, Region, PredictObject
from leaflet.admin import LeafletGeoAdmin


admin.site.register(PObject, LeafletGeoAdmin)
admin.site.register(Region, LeafletGeoAdmin)
admin.site.register(PredictObject, LeafletGeoAdmin)