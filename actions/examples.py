from random import choice
import json


def send_commands_examples(svars, nexa, res):
	with open("data/command_examples.json", "r") as file:
		json_data = json.load(file)
	res.appendText("this is some examples of functional inputs")
	pack = ""
	for idx, intent in enumerate(json_data):
		pack += f"=> {choice(intent)}\n"
		if idx % 3 == 0:
			res.appendText(pack)
			pack = ""
	return res
