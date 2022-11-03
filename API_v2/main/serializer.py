from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import PObject, Region


# class PObjectSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = PObject
#         fields = "__all__"


class PObjectSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PObject
        geo_field = "geometry"
        fields = "__all__"


class RegionSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Region
        geo_field = "geometry"
        fields = "__all__"
