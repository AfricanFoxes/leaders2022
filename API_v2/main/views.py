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
	# get_all_typed_objects(request)
	if request.method == "GET":
		if request.GET.get("o_type"):
			snippets = PObject.objects.filter(type=request.GET.get("o_type"))
			serializer = PObjectSerializer(snippets, many=True)
			return UTF8JsonResponse(serializer.data, safe=False)

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


@csrf_exempt
def get_all_typed_objects(request):
	if request.method == "GET":
		snippets = PObject.objects.values_list('type')
		data = []
		for i in set(snippets):
			_snippets = PObject.objects.filter(type=i[0])
			serializer = PObjectSerializer(_snippets, many=True)
			data.append(serializer.data)
		return UTF8JsonResponse(data, safe=False)



@csrf_exempt
def region_api(request):
	# get_all_typed_objects(request)
	if request.method == "GET":
		if request.GET.get("r_name"):
			snippets = Region.objects.filter(type=request.GET.get("r_name"))
			serializer = RegionSerializer(snippets, many=True)
			return UTF8JsonResponse(serializer.data, safe=False)

		snippets = Region.objects.all()
		serializer = RegionSerializer(snippets, many=True)
		return UTF8JsonResponse(serializer.data, safe=False)

	elif request.method == "POST":
		data = JSONParser().parse(request)
		serializer = RegionSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return UTF8JsonResponse(serializer.data)
		return UTF8JsonResponse(serializer.errors)

