from models.sentence import Sentence
import re



class Analyzer:
	def __init__(self):
		super(Analyzer, self).__init__()
		self.type = Sentence(out="type")
		self.tag = Sentence(out="tag", bag_type="pos")


	def isAboutYou(self, value):
		matches = re.findall(r"(?<![a-zA-Z])(you|your|u)(?![a-zA-Z])", value.lower())
		return bool(len(matches))


	def isNegative(self, value):
		predicted = self.type.predict(value)
		return predicted["type"] == "negative" if predicted else False


	def isQuestion(self, value):
		predicted = self.type.predict(value)
		return predicted["type"] == "question" if predicted else False


	def isAffirmative(self, value):
		predicted = self.type.predict(value)
		return predicted["type"] == "affirmative" if predicted else False


	def isOrder(self, value):
		predicted = self.type.predict(value)
		return predicted["type"] == "order" if predicted else False
