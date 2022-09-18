import re



class Compiler:
	def __init__(self):
		super(Compiler, self).__init__()


	def findVars(self, base_sentence, value):
		svars = {}
		svars["mentions"] = re.findall(r"(@\w+)", value)
		base_sentence = base_sentence.split()
		value = re.sub(r'(@\w+)', '', value) # remove mentions (@)
		value = value.split()
		for startIdx, word in enumerate(base_sentence):
			if "$::" in word:
				key = word.split("::")[1]
				print("base_sentence", base_sentence)
				print("list(reversed(base_sentence))", list(reversed(base_sentence)))
				for endIdx, word in enumerate(reversed(base_sentence)):
					if "$::" in word and key in word:
						try: svars[key] = " ".join(value[startIdx: -endIdx if endIdx != 0 else None])
						except: pass
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
