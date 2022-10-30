from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json


class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


def pull_data(path_file: str):
	with open(path_file, encoding="utf-8") as json_file:
		data = json.load(json_file)
		return data


def all_data(request):
	data = pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")
	return UTF8JsonResponse(data)


def filter_data(request):
	p_type = request.GET.get("p_type")
	
	data = pull_data("/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json")
	filtered_data = [k for k in data['features'] if k["properties"]["type"] == p_type]
	geo_json_data = {"type": "FeatureCollection", "features": filtered_data}
	return UTF8JsonResponse(geo_json_data) 
