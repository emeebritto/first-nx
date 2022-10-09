from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string
import re


with open("base.txt", "r") as file:
	source = file.read()


uInput = input("you: ")
sourceSplited = source.split()
uInputSplited = uInput.split()

print("\n")
print("the next words would be:")
for idx, words in enumerate(sourceSplited):
	if words == uInputSplited[-1]:
		nextWord = sourceSplited[idx:idx + 3]
		print(" ".join(nextWord))
# matches = re.findall(uInputSplited[-1], uInput)
# print(matches)





# # sent_tokens = nltk.sent_tokenize(source)
# # sent_tokens = re.split(r"(?<=,|\.)\s", source)
# sent_tokens = re.split(r"\s", source)
# remove_punct_dict = dict((ord(punct),None) for punct in string.punctuation)
# print("remove_punct_dict", remove_punct_dict)

# def LemNormalize(text):
#   return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

# value = uInput.lower()
# nexa_response = ""
# sent_tokens.append(value)
# print("sent_tokens", sent_tokens)
# tfidfvec = TfidfVectorizer(tokenizer=LemNormalize , stop_words='english')
# tfidf = tfidfvec.fit_transform(sent_tokens)
# val = cosine_similarity(tfidf[-1], tfidf)
# print("val.argsort()", val.argsort())
# idx = val.argsort()[0][-2]
# flat = val.flatten()
# flat.sort()
# score = flat[-2]
# print("score", score)
# if score == 0: nexa_response = "..."
# else: nexa_response = sent_tokens[idx]

# sent_tokens.remove(value)
# print(nexa_response)
