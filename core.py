from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.transformers import answer_by_context
from models.external import Chatbot
from patterns.replacer import replacer
from spaces import question_answering
from utils.response import Response
from googlesearch import search
from bs4 import BeautifulSoup
from compiler import Compiler
from analyzer import Analyzer
from threading import Lock
from mind import Mind
import numpy as np
import requests
import string
import nltk

compiler = Compiler()
chatbot = Chatbot()



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
		self.bert_answer = True
		self.always_use_experimental = False


	@property
	def actions(self):
		return self._actions


	def load(self, subject):
		with open(f"data/{subject}.md", "r") as file:
			return file.read()


	def translate(self, uInput, from_lang='pt', to_lang='en'):
		try:
			result = requests.post(f"https://translater-for-nx.vercel.app/translate?to={to_lang}", { "text": uInput })
			return result.json()["text"]
			# text_to_translate = self._translator.translate(uInput, dest=to_lang)
			# text_to_translate = self._translator.translate(uInput, src=from_lang, dest=to_lang)
		except Exception as e:
			print(f"translate (error): {e}")
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


	def alterProcess(self, value, sender, res):
		value = value.replace("--exp", "")
		about_me = self.load("about_me")
		answer = None
		if self.analyzer.isAboutYou(value):
			answer = question_answering(value, about_me)
			return res.appendText(answer or "I don't know it :(")
		else:
			output = chatbot.input(value, context=sender)
			if not output or not output.get("message"): return res.appendText("tem algo errado comigo, espere uns minutos")
			answer = output["message"]
			answer = self.translate(answer, to_lang="pt")
			return res.appendText(answer or "tem algo errado comigo, espere uns minutos")


	# @_nospam
	def read(self, value, context="", sender="unknown", asyncRes=None, config=None):
		res = Response(asyncRes, config)
		if not value: return res.appendText("...")
		if "exec::" in value.lower(): return self.execCommand(value, sender, res)
		value = self.translate(value, to_lang="en")
		print(f"new message => {value} (author_id: {sender})")
		# analyzed_type = self.analyzer.type.predict(value)
		analyzed_tag = self.analyzer.tag.predict(value) or {}

		if "--exp" in value or self.always_use_experimental:
			return self.alterProcess(value, sender, res) # TEMṔ

		if self.analyzer.isQuestion(value) and self.bert_answer:
			about_me = self.load("about_me")
			other_subject = context + self.nx_search(value) + self.load("other_subject")
			ctx = about_me if self.analyzer.isAboutYou(value) else other_subject 
			answer = question_answering(value, ctx)
			# answer = answer_by_context(
			# 	context=ctx,
			# 	value=value
			# )
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
		res = Response(asyncRes)

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


	def _extractFromText(self, value, source):
		sent_tokens = nltk.sent_tokenize(source)
		remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)

		def LemNormalize(text):
		  return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

		value = value.lower()
		nexa_response = ""
		sent_tokens.append(value)
		tfidfvec = TfidfVectorizer(tokenizer=LemNormalize , stop_words='english')
		tfidf = tfidfvec.fit_transform(sent_tokens)
		val = cosine_similarity(tfidf[-1], tfidf)
		idx = val.argsort()[0][-2]
		flat = val.flatten()
		flat.sort()
		score = flat[-2]
		if score == 0: nexa_response = "sorry, I dont understand"
		else: nexa_response = sent_tokens[idx]

		sent_tokens.remove(value)
		return nexa_response



# git reset --soft HEAD^