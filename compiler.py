class Compiler:
	def __init__(self):
		super(Compiler, self).__init__()


	def findVars(self, base, value):
		svars = {}
		base = base.split()
		value = value.split()
		for idx, word in enumerate(base):
			if "$::" in word:
				key = word.split("::")[1]
				svars[key] = value[idx]
		return svars


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
