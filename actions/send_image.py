import requests



def randonly_image(svars, action):
	res = requests.get("https://picsum.photos/3000/3000/?random")
	return "photo", res.content