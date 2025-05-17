import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room name from the URL
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join the chat room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming messages"""
        data = json.loads(text_data)
        message = data["message"]
        sender = data["sender"]
        print(f"📩 Received in Django: {sender}: {message}")  # ✅ Debugging line

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # This tells Django Channels to call the chat_message method
                "message": message,
                "sender": sender,
            }
        )

        # Acknowledge the message sent successfully
        await self.send(text_data=json.dumps({
            "sender": "server",
            "message": "Message received",
            "acknowledged": True  # Acknowledgment from the server
        }))

    async def chat_message(self, event):
        """Send messages to WebSocket"""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))
    
