from .models import PObject, Region, PredictObject
from .serializer import PObjectSerializer, RegionSerializer, PredictObjectSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.exceptions import ValidationError


class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


@csrf_exempt
def object_api(request):
	if request.method == "GET":
		if request.GET.get("o_type"):
			snippets = PObject.objects.filter(type=request.GET.get("o_type"))
			serializer = PObjectSerializer(snippets, many=True)
			return UTF8JsonResponse(serializer.data, safe=False)

		snippets = PObject.objects.all()
		serializer = PObjectSerializer(snippets, many=True)
		return UTF8JsonResponse(serializer.data, safe=False)

	# elif request.method == "POST":
	# 	data = JSONParser().parse(request)
	# 	serializer = PObjectSerializer(data=data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return UTF8JsonResponse(serializer.data)
	# 	return UTF8JsonResponse(serializer.errors)


@csrf_exempt
def predict_object_api(request):
	if request.method == "GET":
		if request.GET.get("po_type"):
			snippets = PredictObject.objects.filter(type=request.GET.get("po_type"))
			serializer = PredictObjectSerializer(snippets, many=True)
			return UTF8JsonResponse(serializer.data, safe=False)

		snippets = PredictObject.objects.all()
		serializer = PredictObjectSerializer(snippets, many=True)
		return UTF8JsonResponse(serializer.data, safe=False)

	# elif request.method == "POST":
	# 	data = JSONParser().parse(request)
	# 	serializer = PredictObjectSerializer(data=data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return UTF8JsonResponse(serializer.data)
	# 	return UTF8JsonResponse(serializer.errors)


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

	# elif request.method == "POST":
	# 	data = JSONParser().parse(request)
	# 	serializer = RegionSerializer(data=data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return UTF8JsonResponse(serializer.data)
	# 	return UTF8JsonResponse(serializer.errors)


@csrf_exempt
def get_regions_objects(request):
	if request.GET.get("r_name"):
		r_name = request.GET.get("r_name")
		_snippet = Region.objects.filter(NAME=r_name)
		if len(_snippet) != 0:
			okato = list(_snippet)[0].okato
			snippets = PObject.objects.filter(okato=okato)
			serializer = PObjectSerializer(snippets, many=True)
			return UTF8JsonResponse(serializer.data, safe=False)
	return UTF8JsonResponse({"No": "Data"}, safe=False)


K_LAT = 111.134861111
K_LON = 64.87434


def get_items_by_radius(request):
    """
    Выбираем все объекты в квадрате, куда вписана окружность радиуса 3км
    !Важно для быстрого поиска используется поиск не по радиусу а по квадрату
    df - Pandas DataFrame (либо GeoPandas), где объекты имеют колонки долготу "lon" и широту "lat"
    center - центральная точка от которой будут искаться объекты в радиусе
    radius - радиус от центра в км
    """
    center = (float(request.GET.get("lon")), float(request.GET.get("lat")))
    radius = int(request.GET.get("radius"))

    assert center[0] < center[1], "Перепутаны местами долгота широта у `center`, сначала долготу 37.ххх, затем широту 55.ххх"
    min_lon = center[0] - radius/K_LON
    max_lon = center[0] + radius/K_LON
    min_lat = center[1] - radius/K_LAT
    max_lat = center[1] + radius/K_LAT
    data = PObject.objects.filter(lat__gte=min_lat, lat__lte=max_lat, lon__gte=min_lon, lon__lte=max_lon)
    serializer = PObjectSerializer(data, many=True)
    print(len(list(data)))
    # print(snippets[(snippets.lat >= min_lat)&(snippets.lat <= max_lat)&(snippets.lon >= min_lon)&(snippets.lon <= max_lon)])
    return UTF8JsonResponse(serializer.data, safe=False)
