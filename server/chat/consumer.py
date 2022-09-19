import json
from channels.generic import websocket

class ChatRoomConsumer(websocket.AsyncJsonWebsocketConsumer):
  async def connect(self):
    self.room = self.scope["url_route"]["kwargs"]["room"]
    self.room_group = f"chat_{self.room}"
    await self.channel_layer.group_add(
      self.room_group, 
      self.channel_name
    )

    await self.accept()


  async def disconnect(self, code):
    await self.channel_layer.group_discard(
      self.room_group, 
      self.channel_name
    )


  async def receive(self, text_data=None):
    textDataJson = json.loads(text_data)
    message = textDataJson["message"]
    username = textDataJson["username"]

    await self.channel_layer.group_send(
      self.room_group,
      {
        "type": "chat_room_message",
        "message": message,
        'username': username,
      }
    )

  async def chat_room_message(self, event):
    message = event["message"]
    username = event["username"]

    await self.send(text_data=json.dumps({
      "message": message,
      'username': username,
    }))