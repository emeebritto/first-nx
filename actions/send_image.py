import requests
import re
from random import randint


def randonly_image(svars, nexa, res):
	data = requests.get("https://picsum.photos/3000/3000/?random")
	return res.appendPhoto(data.content)


def randonly_face_image(svars, nexa, res):
	source_base = "https://this-person-does-not-exist.com"
	result = requests.get(f"{source_base}/en?new=1663313205973").json()
	data = requests.get(f"{source_base}/{result['src']}")
	return res.appendPhoto(data.content)


def randonly_cat_image(svars, nexa, res):
	source_base = "https://cataas.com/cat"
	data = requests.get(source_base)
	return res.appendPhoto(data.content)


def randonly_cat_gif(svars, nexa, res):
	source_base = "https://cataas.com/cat/gif"
	data = requests.get(source_base)
	return res.appendAnimation(data.content)


def create_image(svars, nexa, res):
	search_url = "https://unsplash.com/napi/search/photos"
	uInput = svars.get("QUERY")
	if not uInput: return res.appendText("sorry, I don't get it :(")
	page = randint(1, 40)
	search_config = f"per_page=1&page={page}&xp=unsplash-plus-2:Control"
	source_base = f"{search_url}?query={uInput}&{search_config}"
	data = requests.get(source_base)
	result_metadata = data.json()["results"][0]
	result_file_url = result_metadata["urls"]["raw"]
	# file = requests.get(result_file_url).content
	result_file_alt = result_metadata.get("alt_description")
	res.appendDocument(result_file_url)
	if result_file_alt: res.appendText(result_file_alt)
	return res.values()
