from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json


class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


def _pull_data(path_file: str):
	with open(path_file, encoding="utf-8") as json_file:
		data = json.load(json_file)
		return data


def get_all_objects(request):
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")
	return UTF8JsonResponse(data)


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


def get_object(request):
	p_type = request.GET.get("p_type")
	
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")
	filtered_data = [k for k in data['features'] if k["properties"]["type"] == p_type]
	geo_json_data = {"type": "FeatureCollection", "features": filtered_data}
	return UTF8JsonResponse(geo_json_data) 


def get_all_regions(request):
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/region.json")
	return UTF8JsonResponse(data)


def get_region(request):
	r_name = request.GET.get("r_name")

	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/region.json")
	filtered_data = [k for k in data['features'] if k["properties"]["NAME"] == r_name]
	geo_json_data = {"type": "FeatureCollection", "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }}, "features": filtered_data}
	return UTF8JsonResponse(geo_json_data)


def get_all_predictions(request):
	data = _pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/predict_postamats.json")
	return UTF8JsonResponse(data)
