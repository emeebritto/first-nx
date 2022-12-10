from utils.functions import syncmethod
from time import sleep
from os import getenv
import requests
import json
import uuid

class Chatbot:
	conversation_id: str
	parent_id: str
	def __init__(self, conversation_id=None):
		self.conversation_id = conversation_id
		self.parent_id = self.generate_uuid()
		self._identify = {}
		self.authorization = ""
		self.cookie = getenv("EXP_COOKIE")
		self._headers = {
			"Host": "chat.openai.com",
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0",
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br",
			"Referer": "https://chat.openai.com/chat",
			"Origin": "https://chat.openai.com",
			"DNT": "1",
			"Connection": "keep-alive",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"Sec-GPC": "1",
			"Pragma": "no-cache",
			"Cache-Control": "no-cache",
			"TE": "trailers"
		}
		self.startTKCicle()


	@property
	def headers(self):
		return {**self._headers}


	def _updateTK(self):
		headers = self.headers
		headers["Cookie"] = self.cookie
		response = requests.get("https://chat.openai.com/api/auth/session", headers=headers)
		cookie = response.headers.get("set-cookie")
		if cookie: self.cookie = cookie
		body = response.json()
		self.authorization = body["accessToken"]


	def generate_uuid(self):
		uid = str(uuid.uuid4())
		return uid


	def getCTX(self, context):
		ctx = self._identify.get(context)
		if ctx: return ctx["conversation_id"], ctx["parent_id"]
		ctx = { "conversation_id": None, "parent_id": self.generate_uuid() }
		self._identify[context] = ctx
		return ctx["conversation_id"], ctx["parent_id"]


	def updateCTX(self, context, conversation_id, parent_id):
		self._identify[context] = {
			"conversation_id": conversation_id,
			"parent_id": parent_id
		}


	@syncmethod
	def startTKCicle(self):
		while True:
			self._updateTK()
			sleep(28*60)


	def input(self, prompt, context="0"):
		conversation_id, parent_id = self.getCTX(context)
		# print(conversation_id, parent_id)
		headers = self.headers
		headers["Authorization"] = "Bearer " + self.authorization
		headers["Cookie"] = self.cookie
		headers["Content-Type"] = "application/json"
		headers["Content-Length"] = "4098"

		data = {
			"action":"next",
			"messages":[
				{"id":str(self.generate_uuid()),
				"role":"user",
				"content":{"content_type":"text","parts":[prompt]}
			}],
			"conversation_id": conversation_id,
			"parent_message_id": parent_id,
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
		self.updateCTX(context, response["conversation_id"], response["message"]["id"])
		message = response["message"]["content"]["parts"][0]
		message = message.replace("OpenAI", "Neblika")
		return {'message':message, 'conversation_id':response["conversation_id"], 'parent_id':self.parent_id}

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
