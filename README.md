<img src="pynet.png">

<h1 align="center">PyNet - High Level Networking Framework (HLNF). [BETA]. <img src="https://www.codefactor.io/repository/github/xzripper/pynet/badge?style=for-the-badge"></h1>

<b><p align="center">
    PyNet is a high level networking framework that provides fast, easy, and clear way to work with network.<br>
    With PyNet you can easily create multiplayer game, chat, or anything you want.<br>
    This framework is based on <a href="https://github.com/kstzl/UrsinaNetworking/">UrsinaNetworking</a> made by <a href="https://github.com/kstzl">kstzl</a>.<br>
    Also improved ```UrsinaNetworking``` by clearing and optimizing the code, improving some code, namings, etc.<br>
    This framework is in BETA and not <i>so stable</i>, so please, report any bugs here. More improvements in future. You can check project TODO below.<br><br></p>
    PyNet technical features:
    <ul>
      <li>Creating server with two lines of code.</li>
      <li>Sending data with any type with one line of code.</li>
      <li>Data-protected when transfering.</li>
      <li>Lot of pre-defined functions.</li>
      <li>All exceptions handled.</li>
      <li>Event-supported.</li>
      <li>Advanced ```disconnect``` feature.</li>
      <li>Much more...</li>
    </ul>

  <br><p align="center">PyNet <a href="https://github.com/xzripper/PyNet/blob/main/documentation.md">documentation</a>.</p>

  <h3 align="center">Example:</h3>

  <p align="center">Client:</p>

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

  <p align="center">Server:</p>

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
</b>

## Project TODO.
- [ ] Client kicked event.
- [ ] Optimize ```easyursinanetworking``` and ```replicated_2```.
- [ ] Implement server closing.
- [ ] Threaded network.
- [ ] Files transfering.
- [ ] Implement UDP connection. (S_DGRAM).
- [ ] Review the code and handle more exceptions.
- [ ] Add game example.
- [ ] Finish project.

<hr><b><p align="center">^_^</p></b>
