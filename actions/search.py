from youtubesearchpython import VideosSearch


def searchVideo(svars, nexa, res):
  query = svars.get("QUERY")
  videosSearch = VideosSearch(query, limit = 3)
  for vid in videosSearch.result()["result"]:
    print(vid)
    res.appendText(f"title: {vid['title']}\nurl: {vid['link']}")
  return res.values()