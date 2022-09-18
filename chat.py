from services.telegram import telegram
from core import Nexa
from actions import nx



nexa = Nexa()
print("Nexa's ready!")

nexa.learnModule(nx)
# nexa.learn("dlvideoyt", dlvideoyt)
# nexa.learn("pronounce_words", pronounce_words)
# nexa.learn("dlmusicyt", dlmusicyt)
# nexa.learn("generate_image", randonly_image)


def telegramChat(update, context):
  print(f"you said \"{update.message.text}\"")
  # print(dir(update.message))
  chatType = update.message.chat.type
  userInput = update.message.text
  if chatType == "supergroup" and not "Nexa" in userInput: return
  res = nexa.read(userInput)

  responsesType = {
    "text": update.message.reply_text,
    "document": update.message.reply_document,
    "video": update.message.reply_video,
    "audio": update.message.reply_audio,
    "photo": update.message.reply_photo,
    "animation": update.message.reply_animation
  }

  for msg in res:
    reply_method = responsesType.get(msg["resType"])
    if reply_method: reply_method(msg["res"])


telegram.onMessage(telegramChat)



# "donwload this video $::URL in $::RESOLUTION",
# "donwload this $::URL in $::RESOLUTION",
# "donwload this media from $::URL in $::RESOLUTION",
# "donwload this video from $::URL in $::RESOLUTION",
# "donwload this video $::URL on $::RESOLUTION",
# "dl this video $::URL in $::RESOLUTION",
# "dl video $::URL in $::RESOLUTION",
# "dl $::URL in $::RESOLUTION"

# supergroup
# private