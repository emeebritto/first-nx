from nexa.telegram import nexaTelegram
from nexa.core import Nexa
# from nexa.compiler import Compiler

# compiler = Compiler()
# result = compiler.translate(
#   value="Russia is your favorite country?",
#   examples=[
#     "Asia is your favorite country ?",
#     "Russia is your favorite country?",
#     "China is your favorite country ?"
#   ]
# )

# print(result)

nexa = Nexa()
print("Nexa's ready!")

while True:
  sentence = nexaTelegram.wait_author_response()
  nexa_msg = nexa.read(sentence)
  nexaTelegram.send_to_author(msg=nexa_msg)
