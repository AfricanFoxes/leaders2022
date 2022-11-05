import json
import requests


def pull(path: str):
	with open(path, "r", encoding="utf-8") as f:
		data = json.load(f)
		return data


def compare():
	data = pull("/Users/ilya/Desktop/out.json")
	data2 = pull("/Users/ilya/Desktop/region.json")

	print(len(data["features"]), len(data2["features"]))

	a = []
	b = []
	for i in data["features"]:
		a.append(i["properties"]["NAME"])
	for i in data2["features"]:
		b.append(i["properties"]["NAME"])

	dif = list(set(b) - set(a))
	print(dif)


def compare2():
	data = pull("/Users/ilya/Desktop/out.json")
	data2 = pull("/Users/ilya/Desktop/objects_dataset.json")

	print(len(data["features"]), len(data2["features"]))

	a = []
	b = []
	for i in data["features"]:
		a.append((i["properties"]["lon"], i["properties"]["lat"], i["properties"]["normalize_name"]))
		# a.append(i["properties"]["normalize_name"])
	for i in data2["features"]:
		b.append((i["properties"]["lon"], i["properties"]["lat"], i["properties"]["normalize_name"]))
		# b.append(i["properties"]["normalize_name"])

	dif = list(set(b) - set(a))
	for i in dif:
		print(f"{i}: {len(i[2])}")


def compare3():
	data2 = pull("/Users/ilya/Desktop/objects_dataset.json")

	doub = []
	for i in data2["features"]:
		if i["properties"]["index"] in doub:
			print(f'{i["properties"]["index"]}    is not one')
		else:
			doub.append(i["properties"]["index"])

if __name__ == '__main__':
	compare2()
