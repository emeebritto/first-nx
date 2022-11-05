from models.transformers import caption_from_image
from utils.functions import create_filePath
import requests
import os


def whatIsOnTheImage(svars, nexa, res):
	imageUrl = svars.get("IMAGE")

	return res.appendText("it's inactive for now.")

	try:
		imgData = requests.get(imageUrl).content
		imagePath = create_filePath(imgData, fileFormat="jpg")
		preds = caption_from_image([imagePath])
		os.remove(imagePath)
		return res.appendText(preds[0])
	except Exception as e:
		print(e)
		return res.appendText("Sorry, I can't get any data from this image.")