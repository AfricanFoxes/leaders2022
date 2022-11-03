import json
import requests


def pull(path: str):
	with open(path, "r", encoding="utf-8") as f:
		data = json.load(f)
		return data


def push():
	data = pull("/Users/ilya/Desktop/objects_dataset.json")
	headers = {'Content-Type': "application/json", 'Accept': "application/json"}

	for i in data["features"]:
		body = i["properties"]
		body["geometry"] = i["geometry"]
		response = requests.post('http://127.0.0.1:8000/api/objects/', json=body, headers=headers)


if __name__ == '__main__':
	push()
