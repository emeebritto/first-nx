from pytube import YouTube
import requests

def dlvideoyt(svars, actions):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="video")
  streams = streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
  stream_target = streams[-1]
  # data = requests.get(stream_target.url, stream=True)
  # print(dir(response))
  # print(response.content)

  print("stream_target", stream_target)
  print("stream_target URL", stream_target.url)

  return "document", stream_target.url

def dlmusicyt(svars, actions):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="audio")
  streams = streams.filter(mime_type="audio/mp4")
  stream_target = streams[0]
  # data = requests.get(stream_target.url, stream=True)
  print("stream_target URL", stream_target.url)

  return "document", stream_target.url