from threading import Thread
import socket
import json
import sys

# HOST = ''  
# PORT = 7000

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print('# Socket created')

# # Create socket on port
# try:
#   s.bind((HOST, PORT))
# except socket.error as msg:
#   print('# Bind failed. ')
#   sys.exit()

# print('# Socket bind complete')

# # Start listening on socket
# s.listen()
# print('# Socket now listening')

# # Wait for client
# conn, addr = s.accept()
# print('# Connected to ' + addr[0] + ':' + str(addr[1]))

# # Receive data from client
# while True:     
#   data = conn.recv(1024)
#   print(dir(conn))
#   conn.send("hello".encode())
#   line = data.decode('UTF-8')    # convert to string (Python 3 only)
#   line = line.replace("\n","")   # remove newline character
#   print( line )

# s.close()


def syncmethod(func):
  def function(*args, **kwargs):
    th = Thread(target=func, args=args, kwargs=kwargs)
    th.start()
  return function


class Socket_Response:
  def __init__(self, conn, req_event):
    super(Socket_Response, self).__init__()
    self.conn = conn
    self.req_event = req_event


  def send(self, data):
    res_json = json.dumps({
      "event": f"_nx_return_event_{self.req_event}_",
      "body": data
    })
    self.conn.send(res_json.encode())


class Socket_Request:
  def __init__(self, conn, event, body):
    super(Socket_Request, self).__init__()
    self.conn = conn
    self.event = event
    self.body = body


class Nx_Socket:
  def __init__(self):
    super(Nx_Socket, self).__init__()
    self.host = ''
    self.methods = {}
    self._onRequest = lambda conn, addr: print("no function was defined")
    self.create_socket()


  def create_socket(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')


  def decode(self, data):
    data = data.decode("UTF-8")
    return json.loads(data)


  def start(self, port):
    self.port = port
    self.server.bind((self.host, port))
    self.server.listen()
    print(f'Socket started (PORT: {port})')
    self._wait_client()


  @syncmethod
  def _wait_client(self):
    while True:
      conn, addr = self.server.accept()
      self._onReturn(conn, addr)


  @syncmethod
  def _onReturn(self, conn, addr):
    while True:
      data = conn.recv(1024)
      if not data: break
      try:
        req_json = self.decode(data)
        req_event = req_json["event"]
        self.methods[req_event](
          Socket_Request(conn, req_event, req_json["body"]),
          Socket_Response(conn, req_event)
        )
      except Exception as e:
        print(e)
        conn.send(json.dumps({"event": "error", "body": "internal error"}).encode())


  def on(self, event, func):
    self.methods[event] = func


  def close(self):
    self.server.close()



def main(req, res):
  print(req.body)
  res.send("hello")

port = int(os.environ.get("PORT", 3080))
socket_server = Nx_Socket()
socket_server.start(port=port)
socket_server.on("message", main)