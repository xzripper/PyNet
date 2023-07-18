from .ursinanetworking import UrsinaNetworkingServer, UrsinaNetworkingClient, UrsinaNetworkingConnectedClient, pynet_log

from .events import SERVER_BROADCAST_EVENT_NAME, SERVER_SENT_DATA_EVENT_NAME

from typing import Union, Callable, Any


class NetServer:
    server: UrsinaNetworkingServer = None

    def __init__(self, ip: str, port: int) -> None:
        """Initialize server."""
        self.server = UrsinaNetworkingServer(ip, port)

    def close(self) -> None:
        """Close server."""
        # self.server.server.close()

        print('NotImplemented.')

    def broadcast(self, data: Any, ignore: list[UrsinaNetworkingConnectedClient]=[]) -> None:
        """Broadcast data to clients."""
        self.server.broadcast(SERVER_BROADCAST_EVENT_NAME, data, ignore)

    def send_data(self, data: Any, client: UrsinaNetworkingConnectedClient) -> None:
        """Send data (message) to client."""
        client.send_message(SERVER_SENT_DATA_EVENT_NAME, data)

    def get_client_id(self, client: UrsinaNetworkingConnectedClient) -> None:
        """Get client ID."""
        return client.id

    def get_client_name(self, client: UrsinaNetworkingConnectedClient) -> None:
        """Get client name."""
        return client.name

    def get_clients(self) -> list[UrsinaNetworkingConnectedClient]:
        """Get list of connected clients."""
        return self.server.clients

    def disconnect_client(self, _client: Union[UrsinaNetworkingClient, UrsinaNetworkingConnectedClient]) -> None:
        """Disconnect client."""
        is_connected = None

        if type(_client) == UrsinaNetworkingServer:
            is_connected = _client.connected

        elif type(_client) == UrsinaNetworkingConnectedClient:
            is_connected = _client.socket.fileno() != -1

        if is_connected:
            if type(_client) == UrsinaNetworkingClient:
                for client in self.get_clients():
                    if client.socket == _client.client:
                        self.server.clients.remove(client)

                        break

            elif type(_client) == UrsinaNetworkingConnectedClient:
                for client in self.get_clients():
                    if client.socket == _client.socket:
                        self.server.clients.remove(client)

                        break

            try:
                if type(_client) == UrsinaNetworkingClient:
                    _client.client().close()

                elif type(_client) == UrsinaNetworkingConnectedClient:
                    _client.socket.close()
            except AttributeError:
                pynet_log('UrsinaNetworkingServer [info/warning] ctx: client.close() (server.py); Connection already closed')

    def process_net(self) -> None:
        """Process net events."""
        self.server.process_net_events()

    def set_on_client_connected(self, handler: Callable):
        """Handle client connection."""
        @self.server.event
        def onClientConnected(client):
            handler(client)

    def set_on_client_disconnected(self, handler: Callable):
        """Handle client disconnection."""
        @self.server.event
        def onClientDisconnected(client):
            handler(client)

    def set_on_client_sent_data(self, handler: Callable):
        """Handle client data transfer."""
        # [CLIENT_SENT_DATA_EVENT_NAME].
        @self.server.event
        def CLIENT_SENT_DATA(client, content):
            handler(client, content)

    @staticmethod
    def static_reply(client: UrsinaNetworkingConnectedClient, data: Any) -> None:
        """Reply to client inside of event."""
        client.send_message(SERVER_SENT_DATA_EVENT_NAME, data)

    @staticmethod
    def static_name(client: UrsinaNetworkingConnectedClient) -> str:
        """Get client name inside of event."""
        return client.name

    @staticmethod
    def static_id(client: UrsinaNetworkingConnectedClient) -> int:
        """Get client ID inside of event."""
        return client.id
