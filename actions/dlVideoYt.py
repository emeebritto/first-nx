from pytube import YouTube

def dlvideoyt(svars, actions):
  video = YouTube(svars.get("URL"))
  streams = video.streams.filter(type="video")
  streams = streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
  stream_target = streams[0]

  return "document", stream_target.url