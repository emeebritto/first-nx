from utils.functions import read_as_binary, create_filePath
from actions.search import VideosSearch
from pytube import YouTube
from api import fileManager
import requests
import os
import re


def searchVideoLink(query):
  videosSearch = VideosSearch(query, limit=1)
  return videosSearch.result()["result"][0]['link']


def createLink(filepath, mime_type, response):
  response.appendText("this file is so large, the telegram just blocked it")
  response.appendText("then, I will create a link to you :)")
  response.appendText("wait a moment..")
  fileManager.addPath(filepath)
  file_url = fileManager.getGFileUrl(filepath, mime_type=mime_type)
  response.appendText(file_url)
  return response.values()


def download_stream(stream_target, ext, res):
  filename = stream_target.get_file_path().split("/")[-1]

  filepath = f"files/{filename}"
  file_infor = {}
  if not fileManager.hasFile(filepath, ext=ext):
    res.appendText("downloading media..")
    stream_target.download("files")
    filepath = fileManager.formatPath(filepath, rename=True, ext=ext)
  else:
    res.appendText("I already have this media.")
    filepath = fileManager.getFileObjByPath(filepath).get("path")

  file_size = os.path.getsize(filepath)
  return filepath, file_size



def dlvideoyt(svars, nexa, res):
  vidUrl = svars.get("URL")
  if "reddit" in vidUrl: return nexa.execute("dlRedditVid", svars, res)
  video = YouTube(vidUrl)
  streams = video.streams.filter(type="video")
  streams = streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
  stream_target = streams[-1]
  filepath, file_size = download_stream(stream_target, ext="mp4", res=res)
  if file_size > 52428800: return createLink(filepath=filepath, mime_type="video/mp4", response=res)
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
  filepath, file_size = download_stream(stream_target, ext="mp3", res=res)
  if file_size > 52428800: return createLink(filepath=filepath, mime_type="audio/mp4", response=res)
  data = read_as_binary(filepath, fileFormat="mp3")
  # data = requests.get(stream_target.url, stream=True)
  print("stream_target URL", stream_target.url)

  return res.appendDocument(data)


def dlRedditVid(svars, nexa, res):
  vidUrl = svars.get("URL")
  resHtml = requests.get(f"https://redditsave.com/info?url={vidUrl.split('?')[0]}").content
  matches = re.findall(r"href=\"(https:\/\/sd\.redditsave\.com.+fallback)\"", str(resHtml))
  print("matches", matches)
  video = requests.get(matches[0]).content
  filepath = create_filePath(video, fileFormat="mp4")
  file_size = os.path.getsize(filepath)
  if file_size > 52428800: return createLink(filepath=filepath, mime_type="video/mp4", response=res)
  return res.appendVideo(read_as_binary(filepath))


def dlMusicByQuery(svars, nexa, res):
  query = svars.get("QUERY")
  if "https://" in query:
    svars["URL"] = query
    return nexa.execute("dlmusicyt", svars, res)
  svars["URL"] = searchVideoLink(f"{query} music audio")
  return nexa.execute("dlmusicyt", svars, res)


def dlVideoByQuery(svars, nexa, res):
  query = svars.get("QUERY")
  if "https://" in query:
    svars["URL"] = query
    return nexa.execute("dlvideoyt", svars, res)
  svars["URL"] = searchVideoLink(query)
  return nexa.execute("dlvideoyt", svars, res)


def dlMusicVideoByQuery(svars, nexa, res):
  query = svars.get("QUERY")
  svars["URL"] = searchVideoLink(f"{query} music")
  return nexa.execute("dlvideoyt", svars, res)