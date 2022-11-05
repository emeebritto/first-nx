from dotenv import load_dotenv
load_dotenv()

from services import telegram
from api import api
from core import Nexa
from actions import nx


nexa = Nexa()
telegram.run()
api.sync_start()
api.keep_wake_up()
nexa.learnModule(nx)
nexa.extend("api", api)


def clearMessages(svars, nexa, res):
  telegram.clearMessages()


nexa.learn("clear_messages", clearMessages)
print("Nexa's ready!")


def inboxChat(msgType, msg):
  if msgType == "text":
    response = nexa.read(value=msg, context="")
    if not response: return "sorry, I don't get it"
    final_response = []
    for part in response:
      if part["msgType"] == "text":
        final_response.append(part["msg"])

    return f"<p>{'</p><p>'.join(final_response)}</p>"


# def telegramChat(user, chat, msgType, msgContent):
def telegramChat(msgType, msg, allMsgs=""):
  if msg.chat.type == "supergroup": return
  chatId = msg.chat.id

  responsesType = {
    "text": msg.reply_text,
    "document": msg.reply_document,
    "video": msg.reply_video,
    "audio": msg.reply_audio,
    "photo": msg.reply_photo,
    "animation": msg.reply_animation
  }


  if msgType == "text":
    nexa.read(
      value=msg.text,
      context=allMsgs,
      sender=chatId,
      asyncRes=responsesType
    )
  elif msgType == "photo":
    nexa.view(
      value=msg.photo,
      instruction=msg.caption,
      sender=chatId,
      asyncRes=responsesType
    )


  # for part in response:
  #   if part["msgType"] == "text":
  #     telegram.registerMsg(f"Nexa said {part['msg']}")

  #   reply_method = responsesType.get(part["msgType"])
  #   if reply_method: reply_method(part["msg"])


telegram.onMessage(telegramChat)
api.inbox.onMessage(inboxChat)


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