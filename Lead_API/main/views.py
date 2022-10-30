from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json


class UTF8JsonResponse(JsonResponse):
    def __init__(self, *args, json_dumps_params=None, **kwargs):
        json_dumps_params = {"ensure_ascii": False, **(json_dumps_params or {})}
        super().__init__(*args, json_dumps_params=json_dumps_params, **kwargs)


def all_data(request):
	with open('/Users/ilya/Documents/GitHub/leaders2022/Lead_API/objects_dataset.json', encoding="utf-8") as json_file:
		data = json.load(json_file)
		return UTF8JsonResponse(data)
