import re
from utils.functions import replace


class Compiler:
	def __init__(self):
		super(Compiler, self).__init__()
		self.examples = []


	def _useExamples(self, examples):
		self.examples = examples


	def translate(self, value, examples):
		self._useExamples(examples)
		""" Asia é seu pais favorito ? """
		""" Russia é seu pais favorito? """
		value = value.split(" ")
		""" ['Asia', 'é', 'seu', 'pais', 'favorito', '?'] """
		""" ['Russia', 'é', 'seu', 'pais', 'favorito?'] """
		variablesZone = self.findVariation(value)
		for idx, zone in enumerate(variablesZone):
			if zone == 1: value[idx] = "$DINAMIC_VALUE"
		""" ['$DINAMIC_VALUE', 'é', 'seu', 'pais', 'favorito?'] """

		value = self._be(value)
		value = self._detectSelf(value)

		return value


	def _be(self, value):
		questionPattern = re.compile(r"(\W|\S)*\sis\s(\W|\S)*\?$")
		getterPattern = re.compile(r"(w|W)hat(\sis|s|'s)\s(\W|\S)*\?$")
		for idx, word in enumerate(value):
			if word == "is":
				if getterPattern.match(" ".join(value)):
					value = replace(r"(w|W)hat(\sis|s|'s)", "*GET", target=value)
					value = replace(r"\?", "", target=value)
				elif questionPattern.match(" ".join(value)):
					value[idx] = "*ISEQUAL"
					value = replace(r"\?", "", target=value)
				else:
					value[idx] = "*SET"
		return value


	def _detectSelf(self, value):
		pattern = re.compile(r"your|you")
		for idx, word in enumerate(value):
			if pattern.match(word): value[idx] = "$SELF"
		return value


	def findVariation(self, value):
		""" sentece """
		variablesZone = [0 for word in value] # example: 1, 0, 0, 0, 0
		for idx, word in enumerate(value):
			for example in self.examples:
				exampleWord = example.split()[idx]
				if self.variartionIndice(word, base=exampleWord) > 1:
					variablesZone[idx] = 1
				else:
					variablesZone[idx] = 0
		return variablesZone


	def variartionIndice(self, target, base):
		""" words """
		variartion = 0
		for idx, letter in enumerate(target):
			try:
				isEqual = base[idx] == letter
				if isEqual: continue
				else: variartion += 1
			except IndexError as e:
				variartion += 1
		return variartion
