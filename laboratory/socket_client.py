from threading import Thread
import socket
import json
import os


# host = ''  # as both code is running on same pc
# port = 7000  # socket server port number

# client_socket = socket.socket()  # instantiate
# client_socket.connect((host, port))  # connect to the server

# message = json.dumps({"event": "message", "body": input(" -> ")}) #  input(" -> ")  # take input

# while message.lower().strip() != 'bye':
#     client_socket.send(message.encode())  # send message
#     # data = client_socket.recv(1024).decode()  # receive response
#     # print('Received from server: ' + data)  # show in terminal

#     message = json.dumps({"event": "message", "body": input(" -> ")})  # again take input

# client_socket.close()  # close the connection



def syncmethod(func):
  def function(*args, **kwargs):
    th = Thread(target=func, args=args, kwargs=kwargs)
    th.start()
  return function



class Nx_Socket_Client:
	def __init__(self):
		super(Nx_Socket_Client, self).__init__()
		self.host = ''
		self.methods = {}
		self._onRequest = lambda conn, addr: print("no function was defined")
		try:
			self.create_socket()
		except socket.error as msg:
			self.client = None
			print(msg)


	def create_socket(self):
		self.client = socket.socket()
		print('Socket created')


	def decode(self, data):
		data = data.decode("UTF-8")
		return json.loads(data)


	def start(self, port):
		self.client.connect((self.host, port))
		print('Socket connected')
		# self._wait_server()


	@syncmethod
	def _wait_server(self):
		while True:
			data = self.client.recv(1024)
			if not data: break
			try:
				res_json = self.decode(data)
				req_event = res_json["event"]
				self.methods[req_event](res_json["body"])
			except Exception as e:
				print("e", e)


	def on(self, event, func):
		self.methods[event] = func


	@syncmethod
	def _emit_fallback(self, event, func):
		data = self.client.recv(1024)
		res_json = self.decode(data)
		if f"_nx_return_event_{event}_" in res_json["event"]:
			func(res_json["body"])


	def emit(self, event, data, await_return=False, fallback=None):
		res_json = json.dumps({"event": event, "body": data})
		self.client.send(res_json.encode())
		if await_return:
			data = self.client.recv(1024)
			res_json = self.decode(data)
			if f"_nx_return_event_{event}_" in res_json["event"]:
				return res_json["body"]
		elif fallback:
			self._emit_fallback(event, fallback)


	def close(self):
		self.client.close()



def main(data):
	print("data", data)
	print("main")


port = int(os.environ.get("PORT", 3080))
sclient = Nx_Socket_Client()
sclient.start(port=port)
sclient.on("message", main)


while True:
	response = sclient.emit("message", input(" -> "), await_return=True)
	print("response", response)


    Flask
    Flask-Login
    Flask-Session
    Flask_SocketIO
    itsdangerous
    Jinja2
    MarkupSafe
    python-engineio
    python-socketio
    six
    Werkzeug
