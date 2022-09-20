from pytube import YouTube
import requests
import os
import re



def read_as_binary(stream, fileFormat):
  stream.download()
  filepath = stream.get_file_path()
  newfilepath = re.sub(r'\.\w*$', f".{fileFormat}", filepath)
  os.rename(filepath, newfilepath)
  data = open(newfilepath, "rb")
  os.remove(newfilepath)
  return data


def dlvideoyt(svars, nexa):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="video")
  streams = streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
  stream_target = streams[-1]
  data = read_as_binary(stream_target, fileFormat="mp4")
  # data = requests.get(stream_target.url, stream=True)
  # print(dir(response))
  # print(response.content)

  print("stream_target", stream_target)
  print("stream_target URL", stream_target.url)

  return [{"msgType": "document", "msg": data}]


def dlmusicyt(svars, nexa):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="audio")
  streams = streams.filter(mime_type="audio/mp4")
  stream_target = streams[0]
  data = read_as_binary(stream_target, fileFormat="mp3")
  # data = requests.get(stream_target.url, stream=True)
  print("stream_target URL", stream_target.url)

  return [{"msgType": "document", "msg": data}]
