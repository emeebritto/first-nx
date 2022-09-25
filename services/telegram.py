from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from dotenv import load_dotenv
from collections import deque
from time import sleep
import requests

from os import getenv
from time import sleep

load_dotenv()

# print(telegram)
# print(dir(telegram))


class Telegram:
	def __init__(self):
		super(Telegram, self).__init__()
		# self.__token = getenv("NxToken")
		self.__token = getenv("ZLToken")
		self.__author = '1242558424'
		self.__author_name = "Emerson_Britto"
		self.notify = lambda msgType, msg: print("no function was defined yet")
		self.messages = {}
		self.updater = Updater(self.__token, use_context=True)
		self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.reply, self._onReply))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self._onMessage))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.photo, self._onPhoto))
		self.updater.start_polling()


	def _onMessage(self, update, context):
		self.notify(
			msgType="text",
			msg=update.message,
		)


	def onMessage(self, func):
		self.notify = func


	def _onPhoto(self, update, context):
		message = update.message
		fileUrl = message.photo[-1].get_file()["file_path"]
		message.photo = fileUrl
		self.notify(
			msgType="photo",
			msg=message,
		)


	def _onReply(self, update, context):
		print("=========== ON REPLY =============")
		print(update.message)


	def start(self, update, context):
		chat = update.message.chat 

		try:
			data = requests.get("https://api.quotable.io/random").json()
			update.message.reply_text(data.get("content"))
		except Exception as e:
			update.message.reply_text(f"Hi {chat.first_name}")


telegram = Telegram()
# print("waiting your message..")
# print(nexa.last_message(user="Emerson-Britto"))
# print(nexa.wait_new_message(user="Emerson_Britto"))
