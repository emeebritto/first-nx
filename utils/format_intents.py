from nltk_utils import tokenords, stem
import json
import uuid


intentsPath = "../data/intents.json"
rawIntentsPath = "../data/intents-raw.json"

with open(rawIntentsPath, 'r') as json_data:
	rawIntents = json.load(json_data)
	formatedIntents = []
	for intent in rawIntents:
		patterns = intent["patterns"]
		base_words = []
		for pattern in patterns:
			base_words.extend(tokenords(pattern))
		base_words = sorted(set([stem(w) for w in base_words]))

		if "$::" in patterns[0]:
			formatedIntents.append({
				"tag": str(uuid.uuid4()),
				"pattern": patterns,
				"execute": intent["execute"],
				"response": intent["response"],
				"base_words": base_words,
				"type": intent["type"]
			})
			continue

		for pattern in patterns:
			formatedIntents.append({
				"tag": str(uuid.uuid4()),
				"pattern": pattern,
				"execute": intent["execute"],
				"response": intent["response"],
				"base_words": base_words,
				"type": intent["type"]
			})

	intents_file = open(intentsPath, "w")
	json.dump(formatedIntents, intents_file, indent=2)
	intents_file.close()
