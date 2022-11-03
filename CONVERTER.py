import json


def pull(path: str):
	with open(path, "r", encoding="utf-8") as f:
		data = json.load(f)
		return data


def convert():
	out = []

	data = pull("/Users/ilya/Desktop/objects_dataset.json")
	for i in range(len(data["features"])):
		out.append(data["features"][i]["properties"])
		out[i]["geometry"] = json.dumps(data["features"][i]["geometry"])
		out[i]["id"] = i

	with open("/Users/ilya/Desktop/out.json", "w") as f:
		json.dump(out, f, ensure_ascii=False)


if __name__ == '__main__':
	convert()