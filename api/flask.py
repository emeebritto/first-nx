# from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, send_file, jsonify
from utils.functions import keep_awake
from .event import Event, Message
from utils.memory import Memory
import os


PORT = int(os.environ.get("PORT", 3080))


flaskAPI = Flask(__name__)
memory = Memory()
setattr(flaskAPI, "keep_awake", keep_awake)
setattr(flaskAPI, "events", Event())


@flaskAPI.route('/', methods=['GET'])
def api_home():
  return "home."


@flaskAPI.route('/test', methods=['GET'])
def api_test():
  return "it looks fine for me."


@flaskAPI.route('/inbox', methods=['GET'])
def api_inbox():
  args = request.args.to_dict()
  msgType = args.get("msgType")
  msg = args.get("msg")

  if not msgType or not msg:
    return "missing queries (required: msgType, msg)"

  message = Message(mType=msgType, text=msg, sender="")

  response = flaskAPI.events.wait_reply(message)
  return jsonify(response)


@flaskAPI.route('/file/<filename>', methods=['GET'])
def files(filename):
  args = request.args.to_dict()
  download = args.get("download")
  filePath = f"files/{filename}"

  try:
    file_data = open(filePath, 'rb')
    memory.reValidateMedia(filePath)
    return send_file(file_data, download_name="nx_file", as_attachment=download)
  except Exception as e:
    print(e)
    return "Sorry, this file does not exist"


@flaskAPI.route('/messages/all', methods=['GET'])
def allMessage():
  args = request.args.to_dict()
  token = args.get("token")
  filePath = f"messages.txt"

  try:
    if token != "y1q8uw2a2023nx": raise Exception("INVALID_TOKEN")
    file_data = open(filePath, 'rb')
    return send_file(file_data, download_name="nx_messages.txt", as_attachment=False)
  except Exception as e:
    print(e)
    return str(e)


memory.start(gap=1)



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