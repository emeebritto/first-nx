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
  print(f"you said {update.message.text}")
  # print(dir(update.message))
  userInput = update.message.text
  resType, res = nexa.read(userInput)

  responsesType = {
    "text": update.message.reply_text,
    "document": update.message.reply_document,
    "video": update.message.reply_video,
    "audio": update.message.reply_audio,
    "photo": update.message.reply_photo
  }

  reply_method = responsesType.get(resType)
  if reply_method: reply_method(res)


telegram.onMessage(telegramChat)



# "donwload this video $::URL in $::RESOLUTION",
# "donwload this $::URL in $::RESOLUTION",
# "donwload this media from $::URL in $::RESOLUTION",
# "donwload this video from $::URL in $::RESOLUTION",
# "donwload this video $::URL on $::RESOLUTION",
# "dl this video $::URL in $::RESOLUTION",
# "dl video $::URL in $::RESOLUTION",
# "dl $::URL in $::RESOLUTION"