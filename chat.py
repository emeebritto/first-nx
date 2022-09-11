from services.telegram import telegram
from core import Nexa


nexa = Nexa()
print("Nexa's ready!")

while True:
  sentence = telegram.wait_author_response()
  res = nexa.read(sentence)
  telegram.send_to_author(msg=res)
