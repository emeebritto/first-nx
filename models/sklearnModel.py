import string
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def skLearnResponse(user_response):
  with open('data/about_me.md', 'r') as f:
    nexaMd = f.read()

  sent_tokens=nltk.sent_tokenize(nexaMd)
  remove_punct_dict=dict( (ord(punct),None) for punct in string.punctuation)
  
  def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))

  user_response=user_response.lower()
  robo_response=''
  sent_tokens.append(user_response)
  tfidfvec=TfidfVectorizer(tokenizer=LemNormalize , stop_words='english')
  tfidf=tfidfvec.fit_transform(sent_tokens)
  val=cosine_similarity(tfidf[-1],tfidf)
  idx=val.argsort()[0][-2]
  flat=val.flatten()
  flat.sort()
  score=flat[-2]
  if score==0:
    robo_response = "sorry, I dont understand"
  else:
    robo_response = sent_tokens[idx]

  sent_tokens.remove(user_response)
  return robo_response