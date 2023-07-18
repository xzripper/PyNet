"""
PyNet.

by xzripper (Github) (UrsinaNetworking - K3#4869 (Discord) / Improved by xzripper (Github)).

Last UrsinaNetworking version: 1.0.5.
Last optimized version: 1.0.
"""

from socket import socket, AF_INET, SOCK_STREAM

from threading import Thread, Lock

from pickle import dumps, loads

from zlib import compress, decompress


MESSAGE_LENGTH = 8
BUFFERSIZE = 4096

BUILTIN_EVENT_CONNECTION_ESTABLISHED = 'onConnectionEstablished'
BUILTIN_EVENT_CONNECTION_ERROR = 'onConnectionError'

BUILTIN_EVENT_CLIENT_CONNECTED = 'onClientConnected'
BUILTIN_EVENT_CLIENT_DISCONNECTED = 'onClientDisconnected'

STATE_HEADER = 'STATE_HEADER'
STATE_PAYLOAD = 'STATE_PAYLOAD'

def pynet_log(msg):
    print(f'PyNet: {msg}')

def ursina_networking_decompress_file(data):
    return decompress(data)

def ursina_networking_encode_file(path):
    file = open(path, 'rb')

    data = file.read()

    file.close()

    return compress(data)

def ursina_networking_encode_message(message, content):
    try:
        message = {
            'Message' : message,
            'Content' : content
        }

        encoded_message = dumps(message)

        message_length = len(encoded_message)

        length_to_bytes = message_length.to_bytes(MESSAGE_LENGTH, byteorder='big')

        final_message = length_to_bytes + encoded_message

        return final_message
    except Exception as e:
        pynet_log(f'ursina_networking_encode_message [error] ctx: encoding message; Error `{e}`.')

    return b''

class UrsinaNetworkingEvents:
    def __init__(self, lock):
        self.events = []

        self.event_table = {}

        self.lock = lock

    def push_event(self, name, *args):
        self.lock.acquire()

        self.events.append((name, args))

        self.lock.release()

    def process_net_events(self):
        self.lock.acquire()

        for event in self.events:
            func = event[0]
            args = event[1]

            try:
                for events in self.event_table:
                    for event in self.event_table[events]:
                        if func in event.__name__:
                            event(*args)
            except Exception as e:
                pynet_log(f'UrsinaNetworkingEvents [error] ctx: processing net events; Error: unable to correctly call function `{e}`.')

        self.events.clear()

        self.lock.release()

    def event(self, func):
        if func.__name__ in self.event_table:
            self.event_table[func.__name__].append(func)

        else:
            self.event_table[func.__name__]= [func]

class UrsinaNetworinkDatagramsBuffer:
    def __init__(self):
        self.header = bytes()
        self.payload = bytes()

        self.buf = bytearray()

        self.pickled_datas = None

        self.payload_length = 0

        self.receive_all = False

        self.datagrams = []

        self.state = STATE_HEADER

    def receive_datagrams(self, client):
        self.buf += client.recv(BUFFERSIZE)

        while True:
            self.state_changed = False

            if self.state == STATE_HEADER:
                if len(self.buf) >= MESSAGE_LENGTH:
                    self.header = self.buf[:MESSAGE_LENGTH]

                    del self.buf[:MESSAGE_LENGTH]

                    self.payload_length = int.from_bytes(self.header, byteorder = 'big', signed = False)

                    self.state = STATE_PAYLOAD

                    self.state_changed = True

            elif self.state == STATE_PAYLOAD:
                if len(self.buf) >= self.payload_length:
                    self.payload = self.buf[:self.payload_length]

                    del self.buf[:self.payload_length]

                    self.state = STATE_HEADER

                    self.state_changed = True

                    self.receive_all = True

                    self.pickled_datas = loads(self.payload)

                    self.datagrams.append(self.pickled_datas)

            if not self.state_changed:
                break

    def receive(self):
        if self.receive_all:
            self.receive_all = False

            return True
        else:
            return False

class UrsinaNetworkingConnectedClient:
    def __init__(self, _socket, address, id):
        self.socket: socket = _socket

        self.address = address

        self.id = id

        self.name = f'Client {id}'

        self.datas = {}

    def __repr__(self):
        return self.name

    def send_message(self, message, content):
        try:
            encoded = ursina_networking_encode_message(message, content)

            self.socket.sendall(encoded)

            return True
        except Exception as e:
            pynet_log(f'UrsinaNetworkingConnectedClient [error] ctx: sending message; Error: `{e}`.')

            return False

class UrsinaNetworkingServer:
    def __init__(self, ip, port):
        self.lock = Lock()

        self.events_manager = UrsinaNetworkingEvents(self.lock)

        self.network_buffer = UrsinaNetworinkDatagramsBuffer()

        self.event = self.events_manager.event

        self.clients = []

        self.lock = Lock()

        try:
            self.server = socket(AF_INET, SOCK_STREAM)

            self.server.bind((ip, port))

            self.server.listen()

            self.receiveThread = Thread(target=self.receive)
            self.receiveThread.start()

            pynet_log(f'Started server with address [{ip}, {port}].')
        except Exception as e:
            pynet_log(f'UrsinaNetworkingServer [error] ctx: init; Cannot create the server: `{e}`.')

    def process_net_events(self):
        self.events_manager.process_net_events()

    def get_client_id(self, client):
        for _client in self.clients:
            if _client.socket == client:
                return _client.id

        return None

    def get_clients_ids(self):
        ret = []

        for client in self.clients:
            ret.append(client.id)

        return ret

    def get_client(self, client):
        for _client in self.clients:
            if _client.socket == client:
                return _client

        return None

    def get_clients(self):
        return self.clients

    def broadcast(self, msg, content, ignore_list=[]):
        for client in self.clients:
            if not client in ignore_list:
                client.send_message(msg, content)

    def handle(self, client):
        while True:
            try:
                self.network_buffer.receive_datagrams(client)

                for datagram in self.network_buffer.datagrams:
                    self.events_manager.push_event(datagram['Message'], self.get_client(client), datagram['Content'])

                self.network_buffer.datagrams = []

            except ConnectionError as e:
                client_copy = self.get_client(client)

                for client in self.clients:
                    if client.socket == client:
                        self.clients.remove(client)

                        break

                try:
                    if type(client) == UrsinaNetworkingClient:
                        client.client().close()

                    elif type(client) == UrsinaNetworkingConnectedClient:
                        client.socket.close()
                except AttributeError:
                    pynet_log('UrsinaNetworkingServer [info/warning] ctx: client.close(); Connection already closed')

                self.events_manager.push_event(BUILTIN_EVENT_CLIENT_DISCONNECTED, client_copy)

                break
            except Exception as e:
                pynet_log(f'UrsinaNetworkingServer [error] ctx: handle; Error: unknown error: `{e}`.')

                break

    def receive(self):
        while True:
            client, address = self.server.accept()

            self.clients.append(UrsinaNetworkingConnectedClient(client, address, len(self.clients)))

            self.events_manager.push_event(BUILTIN_EVENT_CLIENT_CONNECTED, self.get_client(client))

            self.handle_thread = Thread(target = self.handle, args = (client,))
            self.handle_thread.start()

class UrsinaNetworkingClient():
    def __init__(self, ip, port):
        try:
            self.connected = False

            self.lock = Lock()

            self.events_manager = UrsinaNetworkingEvents(self.lock)
            self.network_buffer = UrsinaNetworinkDatagramsBuffer()

            self.event = self.events_manager.event

            self.connected = False

            self.handle_thread = Thread(target = self.handle, args = (ip, port))
            self.handle_thread.start()

            self.lock = Lock()
        except Exception as e:
            pynet_log(f'UrsinaNetworkingClient [error] ctx: client init; Cannot connect to the server: `{e}`.')

    def process_net_events(self):
        self.events_manager.process_net_events()

    def handle(self, ip, port):
        try:
            self.client = socket(AF_INET, SOCK_STREAM)

            self.connection_response = self.client.connect_ex((ip, port))

            if self.connection_response == 0:
                self.connected = True

                self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ESTABLISHED)

                pynet_log('Client connected successfully!')

                while True:
                    try:
                        self.network_buffer.receive_datagrams(self.client)

                        for datagram in self.network_buffer.datagrams:
                            self.events_manager.push_event(datagram['Message'], datagram['Content'])

                        self.network_buffer.datagrams = []

                    except ConnectionError as e:
                        self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ERROR, e)

                        pynet_log(f'UrsinaNetworkingClient [error] ctx: handle; Error: connectionError: Failed to keep the connection with server (Maybe client disconnected?).')

                        break
            else:
                self.events_manager.push_event(BUILTIN_EVENT_CONNECTION_ERROR, self.connection_response)
        except Exception as e:
            self.events_manager.push_event('connectionError', e)

            pynet_log(f'UrsinaNetworkingClient [error] ctx: handle; Error: connection error: `{e}`.')

    def send_message(self, msg, content):
        try:
            if self.connected:
                encoded_message = ursina_networking_encode_message(msg, content)

                self.client.sendall(encoded_message)

                return True
            else:
                pynet_log('UrsinaNetworkingClient [warning] ctx: sending message; Warning: You are trying to send a message but the socket is not connected!')
        except Exception as e:
            pynet_log(f'UrsinaNetworkingClient [error] ctx: message sending; Error: `{e}`.')

            return False
