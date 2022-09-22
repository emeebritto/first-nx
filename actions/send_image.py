import requests
import re
from random import randint


def randonly_image(svars, nexa):
	data = requests.get("https://picsum.photos/3000/3000/?random")
	return [{"msgType": "photo", "msg": data.content}]


def randonly_face_image(svars, nexa):
	source_base = "https://this-person-does-not-exist.com"
	res = requests.get(f"{source_base}/en?new=1663313205973").json()
	data = requests.get(f"{source_base}/{res['src']}")
	return [{"msgType": "photo", "msg": data.content}]


def randonly_cat_image(svars, nexa):
	source_base = "https://cataas.com/cat"
	data = requests.get(source_base)
	return [{"msgType": "photo", "msg": data.content}]


def randonly_cat_gif(svars, nexa):
	source_base = "https://cataas.com/cat/gif"
	data = requests.get(source_base)
	return [{"msgType": "animation", "msg": data.content}]


def create_image(svars, nexa):
	response = []
	search_url = "https://unsplash.com/napi/search/photos"
	uInput = svars.get("QUERY")
	if not uInput: return [{ "msgType": "text", "msg": "sorry, I don't get it :(" }]
	page = randint(1, 40)
	search_config = f"per_page=1&page={page}&xp=unsplash-plus-2:Control"
	source_base = f"{search_url}?query={uInput}&{search_config}"
	data = requests.get(source_base)
	result_metadata = data.json()["results"][0]
	result_file_url = result_metadata["urls"]["raw"]
	# file = requests.get(result_file_url).content
	result_file_alt = result_metadata.get("alt_description")
	response.append({
		"msgType": "document",
		"msg": result_file_url
	})
	if result_file_alt:
		response.append({
			"msgType": "text",
			"msg": result_file_alt
		})

	return response
