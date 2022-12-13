from nltk_utils import tokenords, stem
import json
import uuid


intentsPath = "../data/intents.json"
rawIntentsPaths = [
	"../data/intents-raw.json",
	"../data/dialogs.json"
]


def s_map(pattern):
	sMap = []
	for word in tokenords(pattern):
		if "$::" not in word:
			sMap.append("E")
		else:
			sMap.append("Q")
	return " ".join(sMap)


def create_map(patterns):
	if isinstance(patterns, list):
		maps = []
		for x in patterns:
			maps.append(s_map(x))
		return maps
	else:
		return s_map(patterns)



formatedIntents = []
for rawIntentsPath in rawIntentsPaths:
	with open(rawIntentsPath, 'r') as json_data:
		rawIntents = json.load(json_data)
		for intent in rawIntents:
			patterns = intent["patterns"]
			base_words = []
			for pattern in patterns:
				base_words.extend(tokenords(pattern))
			base_words = sorted(set([stem(w) for w in base_words]))

			if "$::" not in patterns[0]:
				formatedIntents.append({
					"tag": str(uuid.uuid4()),
					"pattern": patterns,
					"map": create_map(patterns),
					"execute": intent["execute"],
					"response": intent["responses"],
					"base_words": base_words,
					"type": intent["type"]
				})
				continue

			for pattern in patterns:
				formatedIntents.append({
					"tag": str(uuid.uuid4()),
					"pattern": pattern,
					"map": create_map(pattern),
					"execute": intent["execute"],
					"response": intent["responses"],
					"base_words": base_words,
					"type": intent["type"]
				})


intents_file = open(intentsPath, "w")
json.dump(formatedIntents, intents_file, indent=2)
intents_file.close()
