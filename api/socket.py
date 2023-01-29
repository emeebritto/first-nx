from flask_socketio import SocketIO, emit, send, disconnect
from utils.functions import keep_awake, syncmethod
from flask_socketio import join_room, leave_room
from utils.managers import Room_Managet
from .event import Event, Message
from api.flask import flaskAPI
from threading import Thread
from flask import request
import os


MAX_BUFFER_SIZE = 2 * 1000 * 1000  # 2 MB
PORT = int(os.environ.get("PORT", 3080))

# 83bf579f570d4747a57bcfe9d409816c

socket = SocketIO(flaskAPI, max_http_buffer_size=MAX_BUFFER_SIZE)
room_Managet = Room_Managet()
setattr(socket, "events", Event())


@socket.on('connect')
def connect():
  print("connected")


@socket.on('connect_to_room')
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


@socket.on('new_message')
def new_message(msgObj):
  msgType = msgObj.get("msgType")
  msgText = msgObj.get("msg")
  socket_id = request.sid

  message = Message(mType=msgType, text=msgText, sender=socket_id)
  socket.events.newMessage(message)


@syncmethod
def start():
  socket.run(flaskAPI, host="0.0.0.0", debug=False, port=PORT)


setattr(socket, "start", start)
setattr(socket, "keep_awake", keep_awake)



# api_Thread = Thread(
# 	target=socketio.run,
# 	args=(api),
# 	kwargs={
# 	  "host": "0.0.0.0",
# 	  "debug": False,
# 	  "port": PORT
# 	}
# )