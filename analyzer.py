from models.sentence import SentenceType


class Analyzer:
	def __init__(self):
		super(Analyzer, self).__init__()
		self.sentence = SentenceType(intentsPath="data/sentence.json", dataPath="data/sentenceType.pth")


	def type(self, value):
		return self.sentence.predict(value)


	def isNegative(self, value):
		predicted = self.sentence.predict(value)
		return predicted["type"] == "negative" if predicted else False


	def isQuestion(self, value):
		predicted = self.sentence.predict(value)
		return predicted["type"] == "question" if predicted else False


	def isAffirmative(self, value):
		predicted = self.sentence.predict(value)
		return predicted["type"] == "affirmative" if predicted else False
