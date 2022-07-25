from nexa.telegram import nexaTelegram
from nexa.core import Nexa

nexa = Nexa()
print("Nexa's ready!")

while True:
  sentence = nexaTelegram.wait_author_response()
  nexa_msg = nexa.read(sentence)
  nexaTelegram.send_to_author(msg=nexa_msg)
