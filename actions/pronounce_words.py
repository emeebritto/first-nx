def pronounce_words(svars, actions):
	word = svars.get("WORD")
	voice = f"https://ssl.gstatic.com/dictionary/static/sounds/20200429/{word}--_us_1.mp3"
	return "document", voice