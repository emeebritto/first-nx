from telegram.ext.updater import Updater
from telegram.update import Update
from telegram import File
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from dotenv import load_dotenv
import requests

from os import getenv
from time import sleep

load_dotenv()

# print(telegram)
# print(dir(telegram))


class Telegram:
	def __init__(self):
		super(Telegram, self).__init__()
		self.__token = getenv("ZLToken") # Zolee
		self.__author = '1242558424'
		self.__author_name = "Emerson_Britto"
		self.onMsgFc = lambda: print("no function was defined")
		self.updater = Updater(self.__token, use_context=True)
		self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self._onMessage))
		self.updater.dispatcher.add_handler(MessageHandler(Filters.photo, self.onPhoto))
		self.updater.start_polling()


	def _onMessage(self, update, context):
		self.onMsgFc(update, context)


	def onMessage(self, func):
		self.onMsgFc = func


	def onPhoto(self, update, context):
		source = update.message.photo[-1].get_file()["file_path"]
		print(source)


	def start(self, update: Update, context: CallbackContext):
		username = update.message.chat.first_name
		data = requests.get("https://api.quotable.io/random").json()
		update.message.reply_text(data.get("content") or f"Hi {username}")


telegram = Telegram()
# print("waiting your message..")
# print(nexa.last_message(user="Emerson-Britto"))
# print(nexa.wait_new_message(user="Emerson_Britto"))