import json
import requests


def pull(path: str):
	with open(path, "r", encoding="utf-8") as f:
		data = json.load(f)
		return data


def compare2():
	data = pull("/Users/ilya/Desktop/out.json")
	data2 = pull("/Users/ilya/Desktop/objects_dataset.json")

	a = []
	b = []
	for i in data["features"]:
		a.append((i["properties"]["lon"], i["properties"]["lat"]))
	for i in data2["features"]:
		b.append((i["properties"]["lon"], i["properties"]["lat"]))

	dif = list(set(b) - set(a))
	return dif


def push_o():
	data = pull("/Users/ilya/Desktop/objects_dataset.json")
	headers = {'Content-Type': "application/json", 'Accept': "application/json"}

	dif = compare2()
	for i in data["features"]:
		if (i["properties"]["lon"], i["properties"]["lat"]) in dif:
			body = i["properties"]
			body["geometry"] = i["geometry"]
			response = requests.post('http://127.0.0.1:8000/api/objects/', json=body, headers=headers)
			print(i["properties"]["name"])


def push_po():
	data = pull("/Users/ilya/Desktop/predict_postamats.json")
	headers = {'Content-Type': "application/json", 'Accept': "application/json"}

	# dif = compare2()
	for i in data["features"]:
		# if (i["properties"]["lon"], i["properties"]["lat"]) in dif:
		body = i["properties"]
		body["geometry"] = i["geometry"]
		response = requests.post('http://127.0.0.1:8000/api/predictions/', json=body, headers=headers)
		# print(i["properties"]["name"])
		print(response.reason)
		input()


def push_r():
	data = pull("/Users/ilya/Desktop/region.json")
	headers = {'Content-Type': "application/json", 'Accept': "application/json"}

	for i in data["features"]:
		body = i["properties"]
		body["geometry"] = i["geometry"]
		response = requests.post('http://127.0.0.1:8000/api/regions/', json=body, headers=headers)
		if response.status_code != 200:
			print(i)
			print(response.raise_for_status)
			input()


if __name__ == '__main__':
	push_po()
