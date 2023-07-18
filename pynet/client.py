from .ursinanetworking import UrsinaNetworkingClient

from .events import CLIENT_SENT_DATA_EVENT_NAME

from typing import Callable, Any


class NetClient:
    client: UrsinaNetworkingClient

    def __init__(self, ip: str, port: int) -> None:
        """Connect to server."""
        self.client = UrsinaNetworkingClient(ip, port)

    def disconnect(self) -> None:
        """Disconnect from server."""
        self.client.client.close()

    def send_data(self, data: Any) -> None:
        """Send data to server."""
        self.client.send_message(CLIENT_SENT_DATA_EVENT_NAME, data)

    def process_net(self) -> None:
        """Process net events."""
        self.client.process_net_events()

    def set_on_server_broadcast(self, handler: Callable) -> None:
        """Handle server broadcast."""
        # [SERVER_BROADCAST_EVENT_NAME].
        @self.client.event
        def SERVER_BROADCAST(content):
            handler(content)

    def set_on_server_sent_data(self, handler: Callable):
        """Handle server data transfer."""
        # [SERVER_SENT_DATA_EVENT_NAME].
        @self.client.event
        def SERVER_SENT_DATA(content):
            handler(content)
