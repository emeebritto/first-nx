from services.telegram import telegram
from core import Nexa


nexa = Nexa()
print("Nexa's ready!")

def say_hi(svars):
  print(svars)
  print("hi")

nexa.learn("say_hi", say_hi)


def chat(update, context):
  print(f"you said {update.message.text}")
  # print(dir(update.message))
  userInput = update.message.text
  res = nexa.read(userInput)
  update.message.reply_text(res)
  # update.message.reply_document(open("profile.png", "rb"))


telegram.onMessage(chat)



# "donwload this video $::URL in $::RESOLUTION",
# "donwload this $::URL in $::RESOLUTION",
# "donwload this media from $::URL in $::RESOLUTION",
# "donwload this video from $::URL in $::RESOLUTION",
# "donwload this video $::URL on $::RESOLUTION",
# "dl this video $::URL in $::RESOLUTION",
# "dl video $::URL in $::RESOLUTION",
# "dl $::URL in $::RESOLUTION"