from threading import Thread
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from utils.functions import interval, wake_up
from .inbox import Inbox

api = Flask(__name__)

def keep_Wake_up():
  interval(wake_up, 4 * 60)


setattr(api, "keep_wake_up", keep_Wake_up)
setattr(api, "inbox", Inbox())


@api.route('/tw', methods=['POST'])
def api_tw():
  incoming_msg = request.values.get('Body', '').lower()
  resp = MessagingResponse()
  msg = resp.message()
  responded = False
  if 'quote' in incoming_msg:
    # return a quote
    r = requests.get('https://api.quotable.io/random')
    if r.status_code == 200:
      data = r.json()
      quote = f'{data["content"]} ({data["author"]})'
    else:
      quote = 'I could not retrieve a quote at this time, sorry.'
    msg.body(quote)
    responded = True
  if 'cat' in incoming_msg:
    # return a cat pic
    msg.media('https://cataas.com/cat')
    responded = True
  if not responded:
    msg.body('I only know about famous quotes and cats, sorry!')
  return str(resp)


@api.route('/test', methods=['GET'])
def api_test():
  return "it looks fine for me."


@api.route('/inbox', methods=['GET'])
def api_inbox():
  args = request.args.to_dict()
  msgType = args.get("msgType")
  msg = args.get("msg")

  if not msgType or not msg: return "missing queries (required: msgType, msg)"

  response = api.inbox.wait_reply(msgType, msg)
  return response



api_Thread = Thread(target=api.run, args=(), kwargs={"host": "0.0.0.0", "debug": False, "port": 3080})
