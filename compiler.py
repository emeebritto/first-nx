import re
from patterns.matcher import matcher
from patterns.replacer import replacer



class Compiler:
	def __init__(self):
		super(Compiler, self).__init__()
		self._examples = []


	def _useExamples(self, examples):
		self._examples = examples


	def toNexa(self, value, base):
		self._useExamples(base)
		""" Asia é seu pais favorito ? """
		""" Russia é seu pais favorito? """
		value = replacer.adjustQuestionMark(value)
		value = value.split(" ")
		""" ['Asia', 'é', 'seu', 'pais', 'favorito', '?'] """
		""" ['Russia', 'é', 'seu', 'pais', 'favorito?'] """
		variablesZone = self.findVariation(value)
		for idx, zone in enumerate(variablesZone):
			if zone == 1: value[idx] = "$DINAMIC_VALUE"
		""" ['$DINAMIC_VALUE', 'é', 'seu', 'pais', 'favorito?'] """

		value = self._be(value)
		value = replacer.setSelfRef(value)

		return value, variablesZone


	def _be(self, value):
		if matcher.getterPattern(value):
			value = replacer.setGetterFlag(value)
			value = replacer.delQuestionMark(value)
		elif matcher.checkPattern(value):
			value = replacer.setComparionFlag(value)
			value = replacer.delQuestionMark(value)
		else:
			value = replacer.setSetterFlag(value)
		return value


	def findVariation(self, value):
		""" sentence """		
		variablesZone = [0 for word in value] # example: 1, 0, 0, 0, 0
		for idx, word in enumerate(value):
			for example in self._examples:
				example = example.split()
				if len(example) == len(value):
					exampleWord = example[idx]
					if self.variationIndice(word, base=exampleWord) > 1:
						variablesZone[idx] = 1
					else:
						variablesZone[idx] = 0
		return variablesZone


	def variationIndice(self, target, base):
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
