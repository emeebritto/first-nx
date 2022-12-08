import requests
import json
import uuid

class Chatbot:
	config: json
	conversation_id: str
	parent_id: str
	def __init__(self, conversation_id=None):
		self.config = self._load_config()
		self.conversation_id = conversation_id
		self.parent_id = self.generate_uuid()

	def _load_config(self):
		with open("config.json", "r") as f:
			config = json.load(f)
		return config

	def generate_uuid(self):
		uid = str(uuid.uuid4())
		return uid
		
	def input(self, prompt):
		Authorization = self.config["Authorization"]
		Cookie = self.config["Cookie"]
		headers = {
			"Host": "chat.openai.com",
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br",
			"Referer": "https://chat.openai.com/chat",
			"Content-Type": "application/json",
			"Authorization": "Bearer " + Authorization,
			"Content-Length": "4098",
			"Origin": "https://chat.openai.com",
			"DNT": "1",
			"Connection": "keep-alive",
			"Cookie": Cookie,
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Sec-GPC": "1",
			"Pragma": "no-cache",
			"Cache-Control": "no-cache",
			"TE": "trailers"
		}
		data = {
			"action":"next",
			"messages":[
				{"id":str(self.generate_uuid()),
				"role":"user",
				"content":{"content_type":"text","parts":[prompt]}
			}],
			"conversation_id":self.conversation_id,
			"parent_message_id":self.parent_id,
			"model":"text-davinci-002-render"
		}
		response = requests.post("https://chat.openai.com/backend-api/conversation", headers=headers, data=json.dumps(data))
		try:
			response = response.text.splitlines()[-4]
		except:
			print(response.text)
			return ValueError("Error: Response is not a text/event-stream")
		try:
			response = response[6:]
		except:
			print(response.text)
			return ValueError("Response is not in the correct format")
		response = json.loads(response)
		self.parent_id = response["message"]["id"]
		self.conversation_id = response["conversation_id"]
		message = response["message"]["content"]["parts"][0]
		message = message.replace("OpenAI", "Neblika")
		return {'message':message, 'conversation_id':self.conversation_id, 'parent_id':self.parent_id}

if __name__ == "__main__":
	print("Type '!exit' to exit")
	chatbot = Chatbot()
	while True:
		prompt = input("You: ")
		if prompt == "!exit":
			break
		try:
			output = chatbot.input(prompt)
		except Exception as e:
			print("Something went wrong!")
			print(e)
			continue
		message = output['message']
		print("Chatbot:", message)
