from youtubesearchpython import VideosSearch
import wikipedia


def searchVideo(svars, nexa, res):
  query = svars.get("QUERY")
  videosSearch = VideosSearch(query, limit = 3)
  result = videosSearch.result()["result"]
  for vid in result:
    res.appendText(f"title: {vid['title']}\nurl: {vid['link']}")
  return res.values()


def searchSummary(svars, nexa, res):
  text = svars.get("TEXT")
  summary = ""
  result = wikipedia.search(text, results = 2)
  for subject in result:
    try:
      summary += wikipedia.summary(subject) + "\n"
    except Exception as e:
      pass
  print(f"detected subject: {result}")
  return summary