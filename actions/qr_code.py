import qrcode


def create_qr_code(svars, actions, nexa):
	data = svars.get("DATA")
	imgPath = "qrcode.png"
	qr = qrcode.QRCode(version=15, box_size=10, border=5)
	qr.add_data(data)
	qr.make(fit=True)
	img = qr.make_image(fill="black", back_color="white")
	img.save(imgPath)
	return [{ "resType": "photo", "res": open(imgPath, "rb") }]