import re


spaced = lambda txt: f" {txt} "


class Replacer:
	def __init__(self):
		super(Replacer, self).__init__()


	def list2str(func):
		def function(*args, **kwargs):
			argsList = list(args)
			if type(argsList[1]) == list: argsList[1] = " ".join(argsList[1])
			result = func(*argsList, **kwargs)
			if type(args[1]) == list: return result.split()
			else: return result
		return function


	@list2str
	def setGetterFlag(self, text):
		""" What is -> *GET """
		return re.sub(r"(w|W)hat(\sis|s|'s)", "*GET", text)


	@list2str
	def setSetterFlag(self, text):
		""" What is -> *GET """
		return re.sub(r"\sis\s", spaced("*SET"), text)


	@list2str
	def setComparionFlag(self, text):
		""" What is -> *GET """
		return re.sub(r"\sis\s", spaced("*ISEQUAL"), text)


	@list2str
	def delQuestionMark(self, text):
		""" ? -> x """
		return re.sub(r"(\?|\s?)", "", text)


	@list2str
	def clearPontuation(self, text):
		return re.sub(r'(\.|\,)', "", text)


	@list2str
	def adjustQuestionMark(self, text):
		return re.sub(r"(?<!\s)(\?(\?*)?)", " ?", text)


	@list2str
	def setSelfRef(self, text):
		""" ? -> x """
		return re.sub(r"\s(your|you)\s", spaced("$SELF"), text)



replacer = Replacer()
