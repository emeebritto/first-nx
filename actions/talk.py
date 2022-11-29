from gtts import gTTS
import uuid
import re



def talk(svars, nexa, res):
	sentence = svars.get("SENTENCE")
	tts = gTTS(text=sentence, lang="en", slow=False)
	filepath = f"{str(uuid.uuid4())}.mp3"
	tts.save(filepath)
	return res.appendAudio(filepath)
