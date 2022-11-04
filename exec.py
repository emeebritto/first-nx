import json
import uuid


intentsPath = "data/sentence.json"


formatedIntents = []
with open(intentsPath, 'r') as json_data:
	rawIntents = json.load(json_data)
	for intent in rawIntents:
		intent["tag"] = str(uuid.uuid4())
		formatedIntents.append(intent)


intents_file = open(intentsPath, "w")
json.dump(formatedIntents, intents_file, indent=2)
intents_file.close()
