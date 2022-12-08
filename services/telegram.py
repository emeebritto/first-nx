from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.ext.filters import Filters
from utils.functions import syncmethod
# from dotenv import load_dotenv
from time import sleep
from os import getenv
import requests

# load_dotenv()



class Telegram:
	def __init__(self):
		super(Telegram, self).__init__()
		# self.__token = getenv("NxToken")
		# self.__token = getenv("ZLToken")
		self.__token = getenv("MkToken")
		self.__author = '1242558424'
		self.__author_name = "Emerson_Britto"
		self._receivers = {}
		self._notify = lambda msgType, msg: print("no function was defined yet")


	@property
	def messages(self):
		with open("messages.txt", "r") as file:
			return file.read()


	def _setReceiver(self, instance):
		self._receivers[instance.chat.id] = instance;


	def _getReceiver(self, idStr):
		return self._receivers.get(idStr)


	def run(self):
		self._updater = Updater(self.__token, use_context=True)
		self._updater.dispatcher.add_handler(CommandHandler('start', self.start))
		self._updater.dispatcher.add_handler(MessageHandler(Filters.reply, self._onReply))
		self._updater.dispatcher.add_handler(MessageHandler(Filters.text, self._onMessage))
		self._updater.dispatcher.add_handler(MessageHandler(Filters.photo, self._onPhoto))
		self._updater.start_polling()


	def registerMsg(self, msg):
		if isinstance(msg, str):
			with open("messages.txt", "a") as file:
				file.write(msg)
				file.write(".\n")


	def clearMessages(self):
		with open("messages.txt", "w") as file:
			file.write("")


	def send(self, mType, msg, to):
		receiver = self._getReceiver(to)
		if not receiver:
			return print("not receiver with this id")
		msgTypes = {
			"text": receiver.reply_text,
			"document": receiver.reply_document,
			"video": receiver.reply_video,
			"audio": receiver.reply_audio,
			"photo": receiver.reply_photo,
			"animation": receiver.reply_animation
		}

		reply_method = msgType.get(mType)
		if reply_method: reply_method(msg)


	@syncmethod
	def _onMessage(self, update, context):
		username = update.message.chat.first_name
		self._setReceiver(update.message)
		self.registerMsg(f"{username} said {update.message.text}")
		self._notify(
			msgType="text",
			msg=update.message,
			allMsgs=self.messages
		)


	def onMessage(self, func):
		self._notify = func


	@syncmethod
	def _onPhoto(self, update, context):
		message = update.message
		fileUrl = message.photo[-1].get_file()["file_path"]
		message.photo = fileUrl
		self._setReceiver(update.message)
		self._notify(
			msgType="photo",
			msg=message,
		)


	def _onReply(self, update, context):
		update.message.reply_text("I don't understand it (reply detected)")


	def start(self, update, context):
		chat = update.message.chat 

		try:
			data = requests.get("https://api.quotable.io/random").json()
			update.message.reply_text(data.get("content"))
		except Exception as e:
			update.message.reply_text(f"Hi {chat.first_name}")
