import requests
import re



def randonly_image(svars, actions, nexa):
	data = requests.get("https://picsum.photos/3000/3000/?random")
	return [{"resType": "photo", "res": data.content}]


def randonly_face_image(svars, actions, nexa):
	source_base = "https://this-person-does-not-exist.com"
	res = requests.get(f"{source_base}/en?new=1663313205973").json()
	data = requests.get(f"{source_base}/{res['src']}")
	return [{"resType": "photo", "res": data.content}]

def randonly_cat_image(svars, actions, nexa):
	source_base = "https://cataas.com/cat"
	data = requests.get(source_base)
	return [{"resType": "photo", "res": data.content}]

def randonly_cat_gif(svars, actions, nexa):
	source_base = "https://cataas.com/cat/gif"
	data = requests.get(source_base)
	return [{"resType": "animation", "res": data.content}]
