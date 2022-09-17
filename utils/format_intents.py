import json
import uuid



intentsPath = "../data/intents.json"
rawIntentsPath = "../data/intents-raw.json"

with open(rawIntentsPath, 'r') as json_data:
	rawIntents = json.load(json_data)["intents"]
	formatedIntents = []
	for intent in rawIntents:
		patterns = intent["patterns"]
		for pattern in patterns:
			formatedIntents.append({
				"tag": str(uuid.uuid4()),
				"pattern": pattern,
				"execute": intent["execute"]
			})

	intents_file = open(intentsPath, "w")
	json.dump({ "intents": formatedIntents }, intents_file, indent=2)
	intents_file.close()
