from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json


class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


# загружает файл json
def _pull_data(path_file: str):
	with open(path_file, encoding="utf-8") as json_file:
		data = json.load(json_file)
		return data


# выдает все объекты
def get_all_objects(request):
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")
	return UTF8JsonResponse(data)


# выдает список объектов отсортивованных по типам
def get_all_typed_objects(request):
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")
	geo_json_data = []
	types = []

	for i in data['features']:
		if i["properties"]["type"] not in types:
			types.append(i["properties"]["type"])

	for i in types:
		filtered_data = [k for k in data['features'] if k["properties"]["type"] == i]
		geo_json_data.append({"type": "FeatureCollection", "features": filtered_data})

	return UTF8JsonResponse({"context": geo_json_data})


# выдает все объекты определенного типа
def get_object(request):
	o_type = request.GET.get("o_type")
	
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")
	filtered_data = [k for k in data['features'] if k["properties"]["type"] == o_type]
	geo_json_data = {"type": "FeatureCollection", "features": filtered_data}
	return UTF8JsonResponse(geo_json_data) 


# выдает все регионы
def get_all_regions(request):
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/region.json")
	return UTF8JsonResponse(data)


# возвращает объект региона
def _get_region_feature(data: dict, r_name: str):
	for i in data["features"]:
		if i["properties"]["NAME"] == r_name:
			return i


# выдает обьект региона в формате geojson
def get_region(request):
	r_name = request.GET.get("r_name")

	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/region.json")

	region_feature = _get_region_feature(data, r_name)

	# filtered_data = [k for k in data['features'] if k["properties"]["NAME"] == r_name]
	geo_json_data = {"type": "FeatureCollection", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }}, "features": [region_feature]}
	return UTF8JsonResponse(geo_json_data)


# выдает лучшие объекты для постамата
def get_all_predictions(request):
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/predict_postamats.json")
	return UTF8JsonResponse(data)


# выдает все объекты входящие в определенный регион
def get_objects_for_region(request):
	r_name = request.GET.get("r_name")
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/region.json")
	data2 = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")

	region_feature = _get_region_feature(data, r_name)

	region_okato = region_feature["properties"]["okato"]

	# region_okato = [k for k in data['features'] if k["properties"]["NAME"] == r_name][0]["properties"]["okato"]
	print(region_okato)
	filtered_data = [k for k in data2['features'] if k["properties"]["okato"] == region_okato]
	geo_json_data = {"type": "FeatureCollection", "features": filtered_data}

	return UTF8JsonResponse(geo_json_data)
