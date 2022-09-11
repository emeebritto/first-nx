from patterns.replacer import replacer
from random import choice
from mind import Mind



class Nexa:
	def __init__(self):
		super(Nexa, self).__init__()
		self._context_network = []
		self.name = "Nexa"
		self.age = 20
		self.context_network = []
		self.mind = Mind(intentsPath="data/intents.json", dataPath="data/data.pth")


	def read(self, value):
		if not value: return ""
		value = replacer.adjustQuestionMark(value)
		predicted = self.Mind.predict(value)
		if not predicted: return "??"
		self.context_network.append(predicted["tag"])
		result = choice(predicted['responses']).split('::')
		context = result[1] if len(result) > 1 else None
		if (context): context_network.append(context)
		return result[0]


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
