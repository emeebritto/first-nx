import requests
import re



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
