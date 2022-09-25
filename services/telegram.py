from telegram.ext.updater import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from utils.functions import syncmethod
from dotenv import load_dotenv
from time import sleep
import requests

from os import getenv
from time import sleep

load_dotenv()



class Telegram:
	def __init__(self):
		super(Telegram, self).__init__()
		# self.__token = getenv("NxToken")
		self.__token = getenv("ZLToken")
		self.__author = '1242558424'
		self.__author_name = "Emerson_Britto"
		self._notify = lambda msgType, msg: print("no function was defined yet")
		self._updater = Updater(self.__token, use_context=True)
		self._updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self._updater.dispatcher.add_handler(MessageHandler(Filters.reply, self._onReply))
		self._updater.dispatcher.add_handler(MessageHandler(Filters.text, self._onMessage))
		self._updater.dispatcher.add_handler(MessageHandler(Filters.photo, self._onPhoto))
		self._updater.start_polling()


	@property
	def messages(self):
		with open("messages.txt", "r") as file:
			return file.read()


	def registerMsg(self, msg):
		if isinstance(msg, str):
			with open("messages.txt", "a") as file:
				file.write(msg)
				file.write(".\n")


	def clearMessages(self):
		with open("messages.txt", "w") as file:
			file.write("")


	@syncmethod
	def _onMessage(self, update, context):
		username = update.message.chat.first_name
		self.registerMsg(f"{username} said {update.message.text}")
		self.notify(
			msgType="text",
			msg=update.message,
			allMsgs=self.messages
		)


	def onMessage(self, func):
		self.notify = func


	@syncmethod
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
