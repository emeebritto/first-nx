# from twilio.twiml.messaging_response import MessagingResponse
from utils.functions import interval, wake_up
from flask import Flask, request, send_file
from threading import Thread
from utils.collector import Collector
from .inbox import Inbox
import requests
import os



api = Flask(__name__)
collector = Collector()

def keep_Wake_up():
  interval(wake_up, 4 * 60)


setattr(api, "keep_wake_up", keep_Wake_up)
setattr(api, "inbox", Inbox())


@api.route('/test', methods=['GET'])
def api_test():
  return "it looks fine for me."


@api.route('/inbox', methods=['GET'])
def api_inbox():
  args = request.args.to_dict()
  msgType = args.get("msgType")
  msg = args.get("msg")

  if not msgType or not msg:
    return "missing queries (required: msgType, msg)"

  response = api.inbox.wait_reply(msgType, msg)
  return response


@api.route('/file/<filename>', methods=['GET'])
def files(filename):
  args = request.args.to_dict()
  download = args.get("download")
  filePath = f"files/{filename}"

  try:
    file_data = open(filePath, 'rb')
    collector.reValidate(path=filePath)
    return send_file(file_data, download_name="NX_file", as_attachment=download)
  except Exception as e:
    print(e)
    return "Sorry, this file does not exist"



port = int(os.environ.get("PORT", 3080))
collector.start(gap=1)
api_Thread = Thread(
  target=api.run,
  args=(),
  kwargs={
    "host": "0.0.0.0",
    "debug": False,
    "port": port
  }
)




# @api.route('/tw', methods=['POST'])
# def api_tw():
#   incoming_msg = request.values.get('Body', '').lower()
#   resp = MessagingResponse()
#   msg = resp.message()
#   responded = False
#   if 'quote' in incoming_msg:
#     # return a quote
#     r = requests.get('https://api.quotable.io/random')
#     if r.status_code == 200:
#       data = r.json()
#       quote = f'{data["content"]} ({data["author"]})'
#     else:
#       quote = 'I could not retrieve a quote at this time, sorry.'
#     msg.body(quote)
#     responded = True
#   if 'cat' in incoming_msg:
#     # return a cat pic
#     msg.media('https://cataas.com/cat')
#     responded = True
#   if not responded:
#     msg.body('I only know about famous quotes and cats, sorry!')
#   return str(resp)