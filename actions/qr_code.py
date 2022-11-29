from utils.functions import create_filePath
import numpy as np
import requests
import qrcode
import uuid
import cv2
import os



def create_qr_code(svars, nexa, res):
	data = svars.get("DATA")
	imgPath = f"{str(uuid.uuid4())}.png"
	qr = qrcode.QRCode(version=15, box_size=10, border=5)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(fill="black", back_color="white")
	img.save(imgPath)
	imgBin = open(imgPath, "rb")
	os.remove(imgPath)
	return res.appendPhoto(imgBin)


def read_qr_code(svars, nexa, res):
	imgPath = svars.get("IMAGE")
	imgUrl = svars.get("URL")
	print("imgPath", imgPath)
	print("imgUrl", imgUrl)	
	imgData = requests.get(imgPath or imgUrl).content
	filePath = create_filePath(data=imgData, fileFormat="jpg")
	img = cv2.imread(filePath)
	os.remove(filePath)
	detector = cv2.QRCodeDetector()
	data, bbox, straight_qrcode = detector.detectAndDecode(img)
	return res.appendText(data)
