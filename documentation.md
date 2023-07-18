<h1 align="center"><b>PyNet Documentation.</b></h1><br>
<h2 align="center"><b>NetServer</b></h2><br>

<p><b>Path: <code>pynet.server</code>.</b></p><br>

<p><b>Server constructor. Creates the server.</b></p>

```python
__init__(self, ip: str, port: int) -> None
```

<p><b>Close the server. [NOT IMPLEMENTED].</b></p>

```python
*-*
```

<p><b>Broadcast data to all clients. Add clients to ignore list to ignore and don't send data to them.</b></p>

```python
broadcast(self, data: Any, ignore: list[UrsinaNetworkingConnectedClient]=[]) -> None
```

<p><b>Send data to specified client.</b></p>

```python
send_data(self, data: Any, client: UrsinaNetworkingConnectedClient) -> None
```

<p><b>Get specified client ID.</b></p>

```python
get_client_id(self, client: UrsinaNetworkingConnectedClient) -> None
```

<p><b>Get specified client name.</b></p>

```python
get_client_name(self, client: UrsinaNetworkingConnectedClient) -> None
```

<p><b>Get all connected clients.</b></p>

```python
get_clients(self) -> list[UrsinaNetworkingConnectedClient]
```

<p><b>Disconnect specified client. [UNSTABLE].</b></p>

```python
disconnect_client(self, _client: Union[UrsinaNetworkingClient, UrsinaNetworkingConnectedClient]) -> None
```

<p><b>Process net events.</b></p>

```python
process_net(self) -> None
```

<p><b>Set on client connected handler. Handler arguments: [CLIENT].</b></p>

```python
set_on_client_connected(self, handler: Callable) -> None
```

<p><b>Set on client disconnected handler. Handler arguments: [CLIENT (can be None)].</b></p>

```python
set_on_client_disconnected(self, handler: Callable) -> None
```

<p><b>Set on client sent data handler. Handler arguments: [CLIENT, DATA].</b></p>

```python
set_on_client_sent_data(self, handler: Callable) -> None
```

<p><b>Static reply to the client. Should be used inside of events (in handlers: like onClientConnected, etc.)</b></p>

```python
@staticmethod static_reply(client: UrsinaNetworkingConnectedClient, data: Any) -> None
```

<p><b>Get name of client inside of event. Should be used inside of events (in handlers: like onClientConnected, etc.)</b></p>

```python
@staticmethod static_name(client: UrsinaNetworkingConnectedClient) -> str
```

<p><b>Get ID of client inside of event. Should be used inside of events (in handlers: like onClientConnected, etc.)</b></p>

```python
@staticmethod static_id(client: UrsinaNetworkingConnectedClient) -> int
```

<br><h2 align="center"><b>NetClient</b></h2><br>

<p><b>Path: <code>pynet.client</code>.</b></p><br>

<p><b>Client constructor. Joins to the server.</b></p>

```python
__init__(self, ip: str, port: int) -> None
```

<p><b>Disconnect from server.</b></p>

```python
disconnect(self) -> None
```

<p><b>Send data to server.</b></p>

```python
send_data(self, data: Any) -> None
```

<p><b>Process net events.</b></p>

```python
process_net(self) -> None
```

<p><b>Set handler on server broadcast. Handler arguments: [DATA].</b></p>

```python
set_on_server_broadcast(self, handler: Callable) -> None
```

<p><b>Set on server sent data handler. Handler arguments: [DATA].</b></p>

```python
set_on_server_sent_data(self, handler: Callable) -> None
```

<br><h2 align="center"><b>Example</b></h2><br>

  <p align="center"><b>Client:</b></p>

  ```python
  from pynet.client import NetClient # Importing.


  client = NetClient('SERVER_IP', 8080) # Joining server.

  def receive_data(data): # On server sent data handler.
      print(f'Got data from server: `{data}`.')

      client.send_data('Did you sent me data?') # Reply to the server.

  def broadcast(data): # On server broadcast handler.
      print(data)

  # Connect handlers.
  client.set_on_server_sent_data(receive_data)

  client.set_on_server_broadcast(broadcast)

  # Process net events. You can also call 'process_net', somewhere in your game loop, or whenever it's good for you.
  while True: client.process_net()
  ```

  <p align="center"><b>Server:</b></p>

  ```python
  from pynet.server import NetServer # Importing.


  server = NetServer('SERVER_IP', 8080) # Creating server.

  def client_connected(client): # On client connected handler.
      NetServer.static_reply(client, 'Hello from server (inside of event)!') # When replying to client inside of event (like onClientConnected), use static_reply.

      server.send_data('Hello from server (during runtime)!', server.get_clients()[0]) # Send data to only one client.

      server.send_data({'x': 0, 'y': 0}, server.get_clients()[0]) # Sending data with any type.

      server.broadcast('Server Broadcast.') # Broadcasting.

  def client_disconnected(client): # On client disconnected handler.
      print(f'Client {NetServer.static_name(client) if client is not None else "Client"} disconnected!') # Print about disconnect.

  def receive_data(client, data): # Client sent data handler.
      print(f'Got data from client with name "{NetServer.static_name(client)}" and id `{NetServer.static_id(client)}`: "{data}".') # Use static_name and static_id to get name and ID inside of event.

  # Connect handlers.
  server.set_on_client_connected(client_connected)
  server.set_on_client_disconnected(client_disconnected)

  server.set_on_client_sent_data(receive_data)

  # Process net events. You can also call 'process_net', somewhere in your game loop, or whenever it's good for you.
  while True: server.process_net()
  ```

<hr><b><p align="center">^_^</p></b>
