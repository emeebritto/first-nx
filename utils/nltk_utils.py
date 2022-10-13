import numpy as np
import nltk
import re
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


def tokenize(sentence):
	"""
	split sentence into array of words/tokens
	a token can be a word or punctuation character, or number
	"""
	print(sentence)
	result = nltk.word_tokenize(sentence)
	print(result)
	return result


def removeVars(sentence):
	if isinstance(sentence, str):
		sentence = re.split(r"\s+", sentence)

	return [word for word in sentence if "$::" not in word]


def tokenords(sentence):
	print(sentence)
	# sentence = re.sub(r"(\s)?\$::[A-Z]*(\s)?", "", sentence)
	sentence = re.sub(r"(?<=\w)\.(?!\w)", " .", sentence)
	sentence = re.sub(r"(?<=\w),+", " ,", sentence)
	sentence = re.sub(r"(?<=\w)\?+", " ?", sentence)
	sentence = re.sub(r"(?<=\w)!+", " !", sentence)
	sentence = re.sub(r"(?<=\w):+(?!\w|[:/])", " :", sentence)
	sentence = re.sub(r"(?<![#%&*])\$+(?=[0-9]{0,})(?!::|\s)", "$ ", sentence)
	sentence = re.sub(r"(?<!\w)#+(?!::|\s|$)", "# ", sentence)
	sentence = re.split(r"\s+", sentence)
	print(sentence)
	return sentence


def stem(word):
	"""
	stemming = find the root form of the word
	examples:
	words = ["organize", "organizes", "organizing"]
	words = [stem(w) for w in words]
	-> ["organ", "organ", "organ"]
	"""
	return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words, tropic_words=None):
	"""
	return bag of words array:
	1 for each known word that exists in the sentence, 0 otherwise
	example:
	sentence = ["hello", "how", "are", "you"]
	words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
	bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
	"""
	# stem each word
	sentence_words = [stem(word) for word in tokenized_sentence]
	print("sentence_words", sentence_words)
	count = 1
	# initialize bag with 0 for each word
	bag = np.zeros(len(words), dtype=np.float32)
	for idx, w in enumerate(words):
		if "$::" not in w and w in sentence_words: 
			bag[idx] = sentence_words.index(w) + 1
			# bag[idx] = count
			# count += 1
			# bag[idx] = 1

	return bag
