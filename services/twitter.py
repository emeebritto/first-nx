from dotenv import load_dotenv
from os import getenv
import tweepy

load_dotenv()



class Twitter:
  @staticmethod
  def init():
    auth = tweepy.OAuthHandler(getenv("TWITTER_KEY"), getenv("TWITTER_SECRET_KEY"))
    # client = tweepy.Client(
    #   consumer_key=getenv("TWITTER_KEY"),
    #   consumer_secret=getenv("TWITTER_SECRET_KEY"),
    #   access_token=getenv("TWITTER_ACCESS_TK"),
    #   access_token_secret=getenv("TWITTER_ACCESS_TK_SECRET")
    # )

    auth.set_access_token(getenv("TWITTER_ACCESS_TK"), getenv("TWITTER_ACCESS_TK_SECRET"))
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
      api.verify_credentials()
      print("Twitter -> Authentication (status: OK)")
      return api
    except Exception as e:
      print("Twitter -> Authentication (status: FAILED)")
      print(f"Reason: {e}")
      raise Exception("Error during authentication")



twitter = Twitter.init()
