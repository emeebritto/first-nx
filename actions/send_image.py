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

# https://this-person-does-not-exist.com/img/avatar-26cbe674bf0a41bf9a750817039c2b65.jpg
# https://this-person-does-not-exist.com/en?new=1663313205973