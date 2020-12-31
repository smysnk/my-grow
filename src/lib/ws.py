from .ws_connection import ClientClosedError
from .ws_server import WebSocketServer, WebSocketClient

class Channel:
  def __init__(self):
    self.clients = []

  def addClient(self, client):
    print("[channel] Adding client (%s)" % (client))
    self.clients.append(client)

  def removeClient(self, client):
    print("[channel] Removing client (%s)" % (client))
    self.clients.remove(client)

  def broadcast(self, payload):
    for client in self.clients:
      client.send(payload)

class Client(WebSocketClient):
  def __init__(self, conn, server):
    super().__init__(conn)
    self.server = server

  def process(self):
    try:
      msg = self.connection.read()
      if not msg:
        return
      msg = msg.decode("utf-8")
      items = msg.split(" ")
      cmd = items[0]
      print(cmd)
    except ClientClosedError:
      self.shutdown()
      self.connection.close()

  def send(self, payload):
    #print("[ws_client] Sending payload (%s)" % (payload))
    self.connection.write(payload)

  def shutdown(self):
    print("[ws_client] Shutting down client (%s)" % (self))
    self.server.remove(self)


class Server(WebSocketServer):
  def __init__(self, channel):
    super().__init__("index.html", 2)
    self.channel = channel

  def _make_client(self, conn):
    client = Client(conn, self)
    self.channel.addClient(client)
    return client

  def remove(self, client):
    self.channel.removeClient(client)
