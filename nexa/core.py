from nexa.brain import NexaBrain
from nexa.compiler import Compiler

compiler = Compiler()

class Nexa(NexaBrain):
	def __init__(self):
		super(Nexa, self).__init__()
		self.name = "Nexa"


	def interpret(self, inputV, outputV, intent):
		""" whats is your favorite country """
		dynamicWords = []
		inputCompiled, variablesZone = compiler.toNexa(
			value=inputV,
			base=intent["patterns"]
		)

		for idx, word in enumerate(inputCompiled):
			if word == "$DYNAMIC_VALUE":
				dynamicWords.append(inputV.split()[idx])
		""" *GET $SELF favorite $DYNAMIC_VALUE """
		""" [0 0 0 0 1] """


	def read(self, value):
		if not value: return ""

		tag, prob = self.predict(value)

		if prob.item() > 0.75:
			for intent in self.intents['intents']:
				hasContext = some_match(self.context_network, intent["context"]) if intent["context"] else True
				if tag == intent["tag"] and hasContext:
					self.context_network.append(intent["tag"])
					response = random.choice(intent['responses'])
					return self.interpret(
						inputV=value,
						outputV=response,
						intent=intent
					)
			return "??"
		else:
			with open('data/about_me.md', 'r') as f:
				nexaMd = f.read()

			return self.extractFromText(value, source=nexaMd)


	def extractFromText(self, value, source):
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
