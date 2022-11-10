# from twilio.twiml.messaging_response import MessagingResponse
from utils.functions import interval, wake_up, syncmethod
from flask import Flask, request, send_file
from flask_socketio import SocketIO, emit, send, disconnect
from flask_socketio import join_room, leave_room
from threading import Thread
from utils.fileManager import FileManager
from utils.managers import Room_Managet
from .inbox import Inbox
import requests
import os

MAX_BUFFER_SIZE = 2 * 1000 * 1000  # 2 MB
# 83bf579f570d4747a57bcfe9d409816c
api = Flask(__name__)
socketio = SocketIO(api, max_http_buffer_size=MAX_BUFFER_SIZE)
fileManager = FileManager()
room_Managet = Room_Managet()

keep_Wake_up = lambda: interval(wake_up, 4 * 60)
setattr(api, "keep_wake_up", keep_Wake_up)
setattr(api, "inbox", Inbox())
setattr(api, "socketio", socketio)


@socketio.on('connect')
def connect():
  print("connected")


@socketio.on('connect_to_room')
def connect_to_room(room_key):
  is_valid = room_Managet.is_valid_key(room_key)
  if is_valid:
    obj_key = room_Managet.get_obj_key(room_key)
    key_label = obj_key["label"].split("::")[1]
    room_Managet.reValidateKey(room_key)
    join_room(room_key)
    response = f"you are connected to your room (key label: {key_label})"
    emit("connected_to_room", response, json=False)
  else:
    response = "your key looks fake, so you can't to enter into room"
    emit("room_key_error", response, json=False)


@api.route('/', methods=['GET'])
def api_home():
  return "home."


@api.route('/test', methods=['GET'])
def api_test():
  return "it looks fine for me."


@api.route('/inbox', methods=['GET'])
def api_inbox():
  args = request.args.to_dict()
  msgType = args.get("msgType")
  msg = args.get("msg")

  if not msgType or not msg:
    return "missing queries (required: msgType, msg)"

  response = api.inbox.wait_reply(msgType, msg)
  return response


@api.route('/file/<filename>', methods=['GET'])
def files(filename):
  args = request.args.to_dict()
  download = args.get("download")
  filePath = f"files/{filename}"

  try:
    file_data = open(filePath, 'rb')
    fileManager.reValidate(path=filePath)
    return send_file(file_data, download_name="nx_file", as_attachment=download)
  except Exception as e:
    print(e)
    return "Sorry, this file does not exist"


@api.route('/messages/all', methods=['GET'])
def allMessage():
  args = request.args.to_dict()
  token = args.get("token")
  filePath = f"messages.txt"

  try:
    if token != "y1q8uw2a2023nx": raise Exception("INVALID_TOKEN")
    file_data = open(filePath, 'rb')
    return send_file(file_data, download_name="nx_messages.txt", as_attachment=False)
  except Exception as e:
    print(e)
    return str(e)


port = int(os.environ.get("PORT", 3080))
fileManager.start(gap=1)

@syncmethod
def start_api():
  socketio.run(api, host="0.0.0.0", debug=False, port=port)
setattr(api, "sync_start", start_api)

api_Thread = Thread(
  target=socketio.run,
  args=(api),
  kwargs={
    "host": "0.0.0.0",
    "debug": False,
    "port": port
  }
)
#Y1q8uw2a%y0q4uw1a#u6
#Y1q8uw2a%y0q4uw1a#p9



# @api.route('/tw', methods=['POST'])
# def api_tw():
#   incoming_msg = request.values.get('Body', '').lower()
#   resp = MessagingResponse()
#   msg = resp.message()
#   responded = False
#   if 'quote' in incoming_msg:
#     # return a quote
#     r = requests.get('https://api.quotable.io/random')
#     if r.status_code == 200:
#       data = r.json()
#       quote = f'{data["content"]} ({data["author"]})'
#     else:
#       quote = 'I could not retrieve a quote at this time, sorry.'
#     msg.body(quote)
#     responded = True
#   if 'cat' in incoming_msg:
#     # return a cat pic
#     msg.media('https://cataas.com/cat')
#     responded = True
#   if not responded:
#     msg.body('I only know about famous quotes and cats, sorry!')
#   return str(resp)