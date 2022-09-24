from utils.functions import read_as_binary
from pytube import YouTube
import requests
import os
import re



def dlvideoyt(svars, nexa, res):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="video")
  streams = streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
  stream_target = streams[-1]
  stream_target.download()
  filepath = stream_target.get_file_path()
  data = read_as_binary(filepath, fileFormat="mp4")
  # data = requests.get(stream_target.url, stream=True)
  # print(dir(response))
  # print(response.content)

  print("stream_target", stream_target)
  print("stream_target URL", stream_target.url)

  return res.appendDocument(data)


def dlmusicyt(svars, nexa, res):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="audio")
  streams = streams.filter(mime_type="audio/mp4")
  stream_target = streams[0]
  stream_target.download()
  filepath = stream_target.get_file_path()
  data = read_as_binary(filepath, fileFormat="mp3")
  # data = requests.get(stream_target.url, stream=True)
  print("stream_target URL", stream_target.url)

  return res.appendDocument(data)
