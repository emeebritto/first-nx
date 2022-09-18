import json



def take_test(svars, actions, nexa):
	res = []
	with open(nexa.intentsPath, "r") as file:
		intents = json.load(file)["intents"]
		for intent in intents:
			msg = {}
			pattern = intent["pattern"]
			print(f"tested pattern: {pattern}")
			predicted = nexa.mind.predict(pattern)
			if pattern != predicted["pattern"] or intent["execute"] != predicted["execute"]:
				msg["resType"] = "text"
				msg["res"] = f"input: {pattern}\npredicted: {predicted['pattern']}\nexpected action: {intent['execute']}\npredicted action: {predicted['execute']}"
				res.append(msg)
	return res
