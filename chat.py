from services.telegram import telegram
from core import Nexa
from actions import nx



nexa = Nexa()
nexa.learnModule(nx)
print("Nexa's ready!")


# def telegramChat(user, chat, msgType, msgContent):
def telegramChat(msgType, msg):
  if msg.chat.type == "supergroup": return
  chatId = msg.chat.id

  if msgType == "text":
    response = nexa.read(value=msg.text, sender=chatId)
    if not response: return
  elif msgType == "photo":
    response = nexa.view(value=msg.photo, instruction=msg.caption, sender=chatId)

  responsesType = {
    "text": msg.reply_text,
    "document": msg.reply_document,
    "video": msg.reply_video,
    "audio": msg.reply_audio,
    "photo": msg.reply_photo,
    "animation": msg.reply_animation
  }

  for part in response:
    reply_method = responsesType.get(part["msgType"])
    if reply_method: reply_method(part["msg"])


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