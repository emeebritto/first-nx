def pronounce_words(svars, actions, nexa):
	word = svars.get("WORD")
	voice = f"https://ssl.gstatic.com/dictionary/static/sounds/20200429/{word}--_us_1.mp3"
	return [{"resType": "document", "res": voice}]