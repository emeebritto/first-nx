import requests
import re



def randonly_image(svars, action):
	res = requests.get("https://picsum.photos/3000/3000/?random")
	return "photo", res.content


def randonly_face_image(svars, action):
	source_base = "https://this-person-does-not-exist.com"
	res = requests.get(f"{source_base}/en?new=1663313205973").json()
	data = requests.get(f"{source_base}/{res['src']}")
	return "photo", data.content
