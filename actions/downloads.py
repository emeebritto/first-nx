from utils.functions import create_filePath
from actions.search import VideosSearch
from pytube import YouTube
from api import memory
import requests
import os
import re



def searchVideoLink(query):
  videosSearch = VideosSearch(query, limit=1)
  return videosSearch.result()["result"][0]['link']


def createLink(filepath, mime_type, response):
  response.sendText("this file is so large, the telegram just blocked it")
  response.sendText("then, I will create a link to you :)")
  response.sendText("wait a moment..")
  memory.putPath(filepath)
  file_url = memory.getHttpUrl(filepath, mime_type=mime_type)
  return response.appendText(file_url)


def download_stream(stream_target, ext, res):
  filename = stream_target.get_file_path().split("/")[-1]

  folderpath = f"files/yt/{ext}" 
  filepath = f"{folderpath}/{filename}"
  file_infor = {}
  if not memory.hasFile(filepath, ext=ext):
    res.sendText("downloading media..")
    stream_target.download(folderpath)
    filepath = memory.formatPath(filepath, rename=True, ext=ext)
  else:
    res.sendText("I already have this media.")
    filepath = memory.getFileObjByPath(filepath).get("path")

  file_size = os.path.getsize(filepath)
  return filepath, file_size


def dlvideoyt(svars, nexa, res):
  vidUrl = svars.get("URL")
  if "reddit" in vidUrl: return nexa.execute("dlRedditVid", svars, res)
  res.sendText("getting stream data from video.")
  video = YouTube(vidUrl)
  streams = video.streams.filter(type="video")
  streams = streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
  stream_target = streams[-1]
  filepath, file_size = download_stream(stream_target, ext="mp4", res=res)
  if file_size > 52428800: return createLink(filepath=filepath, mime_type="video/mp4", response=res)

  # data = requests.get(stream_target.url, stream=True)
  # print(response.content)
  print("stream_target URL", stream_target.url)
  return res.appendDocument(filepath)


def dlmusicyt(svars, nexa, res):
  url = svars.get("URL")
  video = YouTube(url)
  res.sendText("getting stream data from media.")  
  streams = video.streams.filter(type="audio")
  streams = streams.filter(mime_type="audio/mp4")
  stream_target = streams[0]
  filepath, file_size = download_stream(stream_target, ext="mp3", res=res)
  if file_size > 52428800: return createLink(filepath=filepath, mime_type="audio/mp4", response=res)
  # data = requests.get(stream_target.url, stream=True)
  print("stream_target URL", stream_target.url)
  return res.appendDocument(filepath)


def dlRedditVid(svars, nexa, res):
  vidUrl = svars.get("URL")
  folderpath = f"files/rddt/videos"
  resHtml = requests.get(f"https://redditsave.com/info?url={vidUrl.split('?')[0]}").content
  matches = re.findall(r"href=\"(https:\/\/sd\.redditsave\.com.+fallback)\"", str(resHtml))
  video = requests.get(matches[0]).content
  filepath = create_filePath(video, fileFormat="mp4", folder=folderpath)
  file_size = os.path.getsize(filepath)
  if file_size > 52428800: return createLink(filepath=filepath, mime_type="video/mp4", response=res)
  return res.appendVideo(filepath)


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