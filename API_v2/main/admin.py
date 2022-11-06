from django.contrib import admin
from .models import PObject, Region, PredictObject, PredictHexagon
from leaflet.admin import LeafletGeoAdmin


admin.site.register(PObject, LeafletGeoAdmin)
admin.site.register(Region, LeafletGeoAdmin)
admin.site.register(PredictObject, LeafletGeoAdmin)
admin.site.register(PredictHexagon, LeafletGeoAdmin)
