from youtubesearchpython import VideosSearch


def searchVideo(svars, nexa, res):
  query = svars.get("QUERY")
  videosSearch = VideosSearch(query, limit = 3)
  result = videosSearch.result()["result"]
  for vid in result:
    res.appendText(f"title: {vid['title']}\nurl: {vid['link']}")
  return res.values()