try:
  from api.socket import socket
except (ImportError, AttributeError):
  socket = None

try:
  from api.flask import flaskAPI
except ImportError:
  flaskAPI = None
