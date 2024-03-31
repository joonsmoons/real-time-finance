import asyncio
import json
import websockets


class WebSocketConnectionError(Exception):
    """Exception raised for WebSocket connection errors."""


class PolygonApiClient:
    def __init__(self, api_key_id: str):
        """
        Initializes the Polygon API client.

        Args:
            api_key_id (str): API key for authentication.
        """
        self.base_uri = "wss://delayed.polygon.io"
        if api_key_id is None:
            raise Exception("API key cannot be set to None.")
        self.api_key_id = api_key_id

    async def connect_to_websocket(self):
        """
        Connects to the Polygon WebSocket API and performs authentication.
        """
        uri = f"{self.base_uri}/indices"

        while True:
            try:
                self.websocket = await websockets.connect(uri)

                # Authentication message
                auth_message = {"action": "auth", "params": self.api_key_id}
                await self.websocket.send(json.dumps(auth_message))

                # Subscription message for real-time minute aggregates
                subscription_message = {"action": "subscribe", "params": "AM.*"}
                await self.websocket.send(json.dumps(subscription_message))
                break  # If connection and authentication succeed, break the loop
            except Exception as e:
                print(f"Failed to connect to websocket: {e}")
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying

    async def receive_messages(self):
        """
        Receives messages from the connected WebSocket.

        Returns:
            str: The received message.
        """
        if self.websocket is None:
            raise WebSocketConnectionError("WebSocket connection is not established.")

        while True:
            try:
                message = await self.websocket.recv()
                return message
            except websockets.exceptions.ConnectionClosedError:
                raise WebSocketConnectionError(
                    "WebSocket connection closed unexpectedly."
                )
            except Exception as e:
                print(f"Error receiving message: {e}")
                await asyncio.sleep(5)  # Wait for 5 seconds before retrying

    async def close_connection(self):
        """
        Closes the WebSocket connection.
        """
        if self.websocket is not None:
            await self.websocket.close()
            self.websocket = None
