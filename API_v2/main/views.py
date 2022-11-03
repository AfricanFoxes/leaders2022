from django.shortcuts import render
from .models import PObject, Region
from .serializer import PObjectSerializer, RegionSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


@csrf_exempt
def object_api(request):
	if request.method == "GET":
		snippets = PObject.objects.all()
		serializer = PObjectSerializer(snippets, many=True)
		return UTF8JsonResponse(serializer.data, safe=False)
	elif request.method == "POST":
		data = JSONParser().parse(request)
		serializer = PObjectSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return UTF8JsonResponse(serializer.data)
		return UTF8JsonResponse(serializer.errors)


def region_api(request):
	if request.method == "GET":
		snippets = Region.objects.all()
		serializer = RegionSerializer(snippets, many=True)
		return UTF8JsonResponse(serializer.data, safe=False)

