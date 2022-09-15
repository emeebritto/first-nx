from services.telegram import telegram
from core import Nexa
from actions.nx import dlvideoyt, dlmusicyt, pronounce_words


nexa = Nexa()
print("Nexa's ready!")

nexa.learn("dlvideoyt", dlvideoyt)
nexa.learn("dlvideoyt", dlvideoyt)
nexa.learn("dlmusicyt", dlmusicyt)


def chat(update, context):
  print(f"you said {update.message.text}")

  print(dir(update.message))
  userInput = update.message.text
  resType, res = nexa.read(userInput)

  responsesType = {
    "text": update.message.reply_text,
    "document": update.message.reply_document,
    "video": update.message.reply_video,
    "audio": update.message.reply_audio,
  }

  reply_method = responsesType.get(resType)
  if reply_method: reply_method(res)

  # update.message.reply_text(res)
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