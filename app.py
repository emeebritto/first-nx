from dotenv import load_dotenv
load_dotenv()

from utils.response import NxConfig
from api import socket, flaskAPI
from services import telegram
from actions import nx
from core import Nexa
import gradio as gr



nexa = Nexa()
telegram.run()
socket.start()
socket.keep_awake()
nexa.learnModule(nx)


clearMessages = lambda svars, nexa, res: telegram.clearMessages()
nexa.learn("clear_messages", clearMessages)


def apiRequest(msg):
  if msg.type == "text":
    config = NxConfig(file_as="url")
    response = nexa.read(value=msg.text, context="", config=config)
    if not response or not len(response.sequence):
      return [{ "msgType": "text", "msg": "sorry, something is wrong with me" }]
    return response.sequence


def socketRequest(msg):
  print(msgType, msg)

  responsesType = {
    "socket": socket,
  }

  if msg.type == "text":
    config = NxConfig(file_as="url") 
    nexa.read(
      value=msg.text,
      context="",
      sender=msg.sender,
      config=config,
      asyncRes=responsesType
    )


def gradioInteraction(uInput):
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
    "animation": msg.reply_animation,
    "socket": socket,
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
flaskAPI.events.onMessage(apiRequest)
socket.events.onMessage(socketRequest)

nxInterface = gr.Interface(
  fn=gradioInteraction,
  inputs=["text"],
  outputs=["json"]
)

print("Nexa's ready!")
nxInterface.launch()


# def expInteration(uInput, isTrain):
#   return [{ "msgType": "text", "msg": nexa.silly(uInput, train=bool(isTrain)) }]

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