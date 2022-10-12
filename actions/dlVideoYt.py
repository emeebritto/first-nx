from utils.functions import read_as_binary
from api import collector
from pytube import YouTube
import requests
import os
import re



def createLink(path, response):
  new_path = re.sub(r'\s', '-', path)
  new_path = re.sub(r'\!|\?|\#', '', new_path)
  os.rename(path, new_path)

  filename = new_path.split("/")[-1]
  stream_link = f"http://192.168.0.108:3080/file/{filename}"
  download_link = f"http://192.168.0.108:3080/file/{filename}?download=true"
  response.appendText("Sorry, this file is so large, the telegram just blocked it")
  response.appendText("then, I created a link to you :)")
  response.appendText(f"stream: {stream_link}\n\ninstant download: {download_link}")
  collector.addPath(new_path)
  return response.values()


def dlvideoyt(svars, nexa, res):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="video")
  streams = streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
  stream_target = streams[-1]
  stream_target.download("files")
  filename = stream_target.get_file_path().split("/")[-1]
  filepath = f"files/{filename}"
  file_size = os.path.getsize(filepath)
  if file_size > 52428800: return createLink(path=filepath, response=res)
  data = read_as_binary(filepath, fileFormat="mp4")
  # data = requests.get(stream_target.url, stream=True)
  # print(response.content)
  print("stream_target URL", stream_target.url)

  return res.appendDocument(data)


def dlmusicyt(svars, nexa, res):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="audio")
  streams = streams.filter(mime_type="audio/mp4")
  stream_target = streams[0]
  stream_target.download("files")
  filename = stream_target.get_file_path().split("/")[-1]
  filepath = f"files/{filename}"
  file_size = os.path.getsize(filepath)
  if file_size > 52428800: return createLink(path=filepath, response=res)
  data = read_as_binary(filepath, fileFormat="mp3")
  # data = requests.get(stream_target.url, stream=True)
  print("stream_target URL", stream_target.url)

  return res.appendDocument(data)
