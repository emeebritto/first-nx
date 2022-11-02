from utils.functions import read_as_binary
from utils.managers import Room_Managet
from pytube import YouTube
from api import collector, socketio
import os
import re
room_Managet = Room_Managet()


def no_url(res):
	res.appendText("I can't get any url from it")
	res.appendText("try again")
	return res.values()


def no_label(res):
	res.appendText("I can't identify your room")
	res.appendText("try again")
	return res.values()


def createLink(path, res):
  new_path = re.sub(r'\s', '-', path)
  new_path = re.sub(r'\!|\?|\#|�|&|ø', '', new_path)
  new_path = re.sub(r'\.\w*$', ".mp3", new_path)
  os.rename(path, new_path)

  filename = new_path.split("/")[-1]
  stream_link = f"http://127.0.0.1:3080/file/{filename}"
  # stream_link = f"https://nexa-shi.herokuapp.com/file/{filename}"
  collector.addPath(new_path)
  return stream_link


def play_sound(svars, nexa, res):
	url = svars.get("URL")
	sender_id = svars.get("SENDER_ID")
	label = svars.get("LABEL")

	if not url: return no_url(res)	
	if not label: return no_label(res)

	video = YouTube(url)
	streams = video.streams.filter(type="audio")
	streams = streams.filter(mime_type="audio/mp4")
	stream_target = streams[0]
	stream_target.download("files")
	filename = stream_target.get_file_path().split("/")[-1]
	filepath = f"files/{filename}"
	# data = read_as_binary(filepath, fileFormat="mp4")
	response = createLink(path=filepath, res=res)
	obj_key = room_Managet.get_key(f"{sender_id}::{label}")
	if not obj_key: return no_label(res)
	order = {
		"label": "play_audio",
		"data": response
	}
	socketio.emit("execute_order", order, to=obj_key["key"])
	key_label = obj_key['label'].split('::')[1]
	return res.appendText(f"playing audio on your {key_label}")


def stop_sound(svars, nexa, res):
	sender_id = svars.get("SENDER_ID")
	label = svars.get("LABEL")
	if not label: return no_label(res)

	obj_key = room_Managet.get_key(f"{sender_id}::{label}")
	if not obj_key: return no_label(res)
	socketio.emit("execute_order", {"label":"stop_audio"}, to=obj_key["key"])


def pause_sound(svars, nexa, res):
	sender_id = svars.get("SENDER_ID")
	label = svars.get("LABEL")
	if not label: return no_label(res)

	obj_key = room_Managet.get_key(f"{sender_id}::{label}")
	if not obj_key: return no_label(res)
	socketio.emit("execute_order", {"label":"pause_audio"}, to=obj_key["key"])


def resume_sound(svars, nexa, res):
	sender_id = svars.get("SENDER_ID")
	label = svars.get("LABEL")
	if not label: return no_label(res)

	obj_key = room_Managet.get_key(f"{sender_id}::{label}")
	if not obj_key: return no_label(res)
	socketio.emit("execute_order", {"label":"resume_audio"}, to=obj_key["key"])
