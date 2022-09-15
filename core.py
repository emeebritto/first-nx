import string
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from compiler import Compiler
from patterns.replacer import replacer
from random import choice
from mind import Mind

compiler = Compiler()



class Nexa:
	def __init__(self):
		super(Nexa, self).__init__()
		self._context_network = []
		self.name = "Nexa"
		self.age = 20
		self._actions = {}
		self.mind = Mind(intentsPath="data/intents.json", dataPath="data/data.pth")


	def read(self, value):
		if not value: return "None", ""
		value = replacer.adjustQuestionMark(value)
		predicted = self.mind.predict(value)
		if not predicted: return "text", "??"
		svars = compiler.findVars(predicted["pattern"], value)
		print("svars", svars)
		action = predicted.get("execute")
		if action: return self.execute(action, svars)
		return resType, res


	def learn(self, label, action):
		print(f"{self.name} learned to {label}")
		self._actions[label] = action


	def execute(self, label, svars):
		action = self._actions.get(label)
		if action: return action(svars, self._actions)


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
