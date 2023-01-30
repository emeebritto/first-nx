from spaces import question_answering
from utils.response import Response
from models.BiLSTM_crf import NER
from googlesearch import search
from bs4 import BeautifulSoup
from compiler import Compiler
from analyzer import Analyzer
from models.core import Silly
from threading import Lock
from mind import Mind
import requests


compiler = Compiler()


class Nexa(Mind):
	def __init__(self):
		super(Nexa, self).__init__()
		self._context_network = []
		self.name = "Nexa"
		self.me = self.load("about_me")
		self._actions = {}
		self.pending = {}
		self._requests_active = []
		self._lock = Lock()
		self.analyzer = Analyzer()
		self.ner = NER()
		self.silly = Silly()
		self.bert_answer = True
		self.always_use_experimental = False


	@property
	def actions(self):
		return self._actions


	def load(self, subject):
		with open(f"data/{subject}.md", "r") as file:
			return file.read()


	def translate(self, uInput, from_lang='pt', to_lang='en', case=None, case_enclude=""):
		if case or case_enclude and case_enclude in uInput:
			try:
				result = requests.post(f"https://translater-for-nx.vercel.app/translate?to={to_lang}", { "text": uInput })
				return result.json()["text"]
			except Exception as e:
				print(f"translate (error): {e}")
				return uInput
		else:
			return uInput


	def _nospam(func):
		def function(*args, **kwargs):
			sender = kwargs.get("sender", "unknown")
			nexa = args[0]
			nexa._requests_active.append(sender)
			if sender in nexa._requests_active:
				nexa._lock.acquire()

			try: returned = func(*args, **kwargs)
			except Exception as e:
				returned = None
				print(e)

			try: nexa._lock.release()
			except: pass
			nexa._requests_active.remove(sender)
			return returned
		return function


	def nx_search(self, value):
		def page_content(url):
		  thepage = requests.get(url).content
		  soup = BeautifulSoup(thepage, "html.parser")
		  return soup.text

		source = ""
		urls = [*search(value, 2)]
		for url in urls:
			print(f"nexa searched: {url}")
			source += page_content(url)
		return source


	# @_nospam
	def read(self, value, context="", sender="unknown", asyncRes=None, config=None):
		res = Response(sender, asyncRes, config)
		if not value: return res.appendText("...")
		if "exec::" in value.lower(): return self.execCommand(value, sender, res)
		value = self.translate(value, to_lang="en", case_enclude="--tr")
		print(f"new message => {value} (author_id: {sender})")
		analyzed_tag = self.analyzer.tag.predict(value) or {}

		# output = self.ner.predict(value)
		# print(" ".join(output))
		# return res.appendText(" ".join(output))

		if self.analyzer.isQuestion(value) and self.bert_answer:
			about_me = self.load("about_me")
			other_subject = context + self.nx_search(value) + self.load("other_subject")
			ctx = about_me if self.analyzer.isAboutYou(value) else other_subject 
			answer = question_answering(value, ctx)
			return res.appendText(answer or "I don't know it :(")

		predicted = self.predict(value).high_precision(base=analyzed_tag.get("base_words"))
		if not predicted.intent: return res.appendText("??")

		print("predicted intent", predicted.intent)
		svars = compiler.findVars(predicted.intent["pattern"], value)
		pendingVars = self.pending.get(sender)

		if pendingVars:
			svars[pendingVars["name"]] = pendingVars["value"]
			del self.pending[sender]
			
		print("svars", svars)
		svars["SENDER_ID"] = sender
		action = predicted.intent.get("execute")
		if action: self.execute(action, svars, res)

		responses = predicted.intent.get("response")
		if responses: res.appendText(responses, choiceOne=True)
		return res


	def view(self, value, instruction=None, sender="unknown", asyncRes=None):
		if not value: return
		res = Response(sender, asyncRes)

		return res.appendText("my vision system is desabled, i don't see anything")

		if instruction:
			predicted = self.predict(instruction)
			if not predicted: res.appendText("??")
			svars = compiler.findVars(predicted["pattern"], value)
			svars["IMAGE"] = value
			action = predicted.get("execute")
			if action: return self.execute(action, svars, res)
		else:
			res.appendText("what do I do with it?")

		self.pending[sender] = {
			"name": "IMAGE",
			"value": value
		}

		return res.values()


	def learnModule(self, module):
		for name, val in module.__dict__.items():
			if callable(val): self.learn(label=name, action=val)


	def extend(self, attr, value):
		setattr(self, attr, value)


	def learn(self, label, action):
		print(f"{self.name} learned to {label}")
		self._actions[label] = action


	def execCommand(self, value, sender, res):
		svars = {}
		params = value.split("::")
		action = params[1].lower()
		actionParams = params[2:]
		for idx in range(0, len(actionParams), 2):
			var_name = actionParams[idx].upper()
			var_val = actionParams[idx+1]
			svars[var_name] = var_val
			svars[var_val] = var_name # bidirectional
		svars["SENDER_ID"] = sender
		return self.execute(action, svars, res)


	def execute(self, label, svars, res):
		action = self._actions.get(label)
		if action: return action(svars, self, res)
		res.appendText(f"action not found. ({label})")



# git reset --soft HEAD^
