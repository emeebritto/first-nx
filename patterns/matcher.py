import re


class Matcher:
	def __init__(self):
		super(Matcher, self).__init__()


	def list2str(func):
		def function(*args, **kwargs):
			argsList = list(args)
			if type(argsList[1]) == list: argsList[1] = " ".join(argsList[1])
			return func(*argsList, **kwargs)
		return function


	@list2str
	def checkPattern(self, text):
		""" ... is ... ? """
		checkPattern = re.compile(r"(\W|\S)*(?<!(w|W)hat)\sis\s(\W|\S)*\?$")
		return checkPattern.match(text)


	@list2str
	def getterPattern(self, text):
		""" What is ... ? """
		getterPattern = re.compile(r"(w|W)hat(\sis|s|'s)\s(\W|\S)*\?$")
		return getterPattern.match(text)



matcher = Matcher()
