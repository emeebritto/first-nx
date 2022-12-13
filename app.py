from dotenv import load_dotenv
load_dotenv()

from utils.response import NxConfig
from services import telegram
from actions import nx
from core import Nexa
from api import api
# from models.BiLSTM_crf import NER
import gradio as gr


nexa = Nexa()
telegram.run()
api.sync_start()
api.keep_wake_up()
nexa.learnModule(nx)
nexa.extend("api", api)
# ner = NER()
# ner.train()
# while True:
#   uInput = input("you: ")
#   out = ner.predict(uInput)
#   print(out)

def clearMessages(svars, nexa, res):
  telegram.clearMessages()


nexa.learn("clear_messages", clearMessages)
print("Nexa's ready!")


def inboxChat(msgType, msg):
  if msgType == "text":
    config = NxConfig(file_as="url")
    response = nexa.read(value=msg, context="", config=config)
    if not response or not len(response.sequence):
      return [{ "msgType": "text", "msg": "sorry, something is wrong with me" }]
    return response.sequence


def interaction(uInput):
  config = NxConfig(file_as="url")
  response = nexa.read(value=uInput, context="", config=config)
  if not response or not len(response.sequence):
    return [{ "msgType": "text", "msg": "sorry, something is wrong with me" }]
  return response.sequence


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

nxapp = gr.Interface(fn=interaction, inputs="text", outputs=["json"])
nxapp.launch()


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