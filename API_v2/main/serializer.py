from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import PObject, Region, PredictObject, PredictHexagon


class PObjectSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PObject
        geo_field = "geometry"
        fields = "__all__"


class PredictObjectSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PredictObject
        geo_field = "geometry"
        fields = "__all__"


class PredictHexagonSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PredictHexagon
        geo_field = "geometry"
        fields = "__all__"


class PredictHexagonHEATMAPSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PredictHexagon
        geo_field = "geometry"
        fields = ("lon", "lat", "ensemble_predict", "forest_predict")


class RegionSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Region
        geo_field = "geometry"
        fields = "__all__"
