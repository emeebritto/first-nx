from random import randint
from os import getenv
import requests
import base64
import json
import re


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
	try:
		data = requests.get(source_base)
		return res.appendAnimation(data.content)
	except Exception as e:
		return res.appendText("sorry, but I think there was an Error during the process.")


def randonly_dog_image(svars, nexa, res):
	source_base = "https://dog.ceo/api/breeds/image/random"
	data = requests.get(source_base).json()
	return res.appendPhoto(data.message)


def download_image(svars, nexa, res):
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


def create_image(svars, nexa, res):
	uInput = svars.get("INPUT")
	print({ "uInput": uInput })
	if not uInput: return res.appendText("Sorry, I don't understand you")
	res.appendText("processing (8 - 40 seconds)")
	data = requests.post(getenv("CREATE_IMAGE_URL"), headers={
	  "Host": "stabilityai-stable-diffusion.hf.space",
	  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
	  "Accept": "*/*",
	  "Accept-Language": "en-US,en;q=0.5",
	  "Accept-Encoding": "gzip, deflate, br",
	  "Referer": f"{getenv('CREATE_IMAGE_ORIGIN')}/?__theme=light",
	  "Content-Type": "application/json",
	  "Content-Length": "53",
	  "Origin": getenv("CREATE_IMAGE_ORIGIN"),
	  "DNT": "1",
	  "Connection": "keep-alive",
	  "Cookie": f"session-space-cookie={getenv('CREATE_IMAGE_SESSION_COOKIE')}",
	  "Sec-Fetch-Dest": "empty",
	  "Sec-Fetch-Mode": "cors",
	  "Sec-Fetch-Site": "same-origin",
	  "Sec-GPC": "1",
	  "TE": "trailers"
	}, data=json.dumps({"fn_index":2,"data":[uInput],"session_hash":getenv("CREATE_IMAGE_SESSION_HASH")}))
	data = data.json()
	for base in data["data"][0]:
		formatted_base = base.replace("data:image/jpeg;base64,", "")
		res.appendPhoto(base64.decodebytes(bytes(formatted_base, "utf-8")))
