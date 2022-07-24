from nexa import nexa
import nltk
import random
import json

import torch

from models.model import NeuralNet
from utils.nltk_utils import bag_of_words, tokenize
from models.sklearnModel import skLearnResponse

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def some_match(list1, list2):
  for item in list1:
    if item in list2: return True
  return False

with open('data/intents.json', 'r') as json_data:
  intents = json.load(json_data)

FILE = "data/data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Nexa"
print("Nexa's ready!")

context_network = []

while True:
  sentence = nexa.wait_author_response()
  if not sentence: continue

  tokenized_sentence = tokenize(sentence)
  X = bag_of_words(tokenized_sentence, all_words)
  X = X.reshape(1, X.shape[0])
  X = torch.from_numpy(X).to(device)

  output = model(X)
  _, predicted = torch.max(output, dim=1)

  tag = tags[predicted.item()]
  probs = torch.softmax(output, dim=1)
  prob = probs[0][predicted.item()]
  if prob.item() > 0.75:
    for intent in intents['intents']:
      hasContext = some_match(context_network, intent["context"]) if intent["context"] else True
      if tag == intent["tag"] and hasContext:
        context_network.append(intent["tag"])
        result = random.choice(intent['responses']).split('::')
        response = result[0]
        context = result[1] if len(result) > 1 else None
        if (context): context_network.append(context)
        # print(response, context)
        nexa.send_to_author(msg=response)
      elif tag == intent["tag"]:
        nexa.send_to_author(msg="??")
  else:
    nexa.send_to_author(msg=skLearnResponse(sentence))
