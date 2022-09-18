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

    await self.channel_layer.group_send(
      self.room_group, 
      {
        "type": "chat_room_message",
        "tester": " tester"
      }
    )
    

  async def disconnect(self, code):
    await self.channel_layer.group_discard(
      self.room_group, 
      self.channel_name
    )


  async def receive(self, text_data=None, bytes_data=None, **kwargs):
    return await super().receive(text_data, bytes_data, **kwargs)

  async def chat_room_message(self, event):
    tester = event["tester"]

    await self.send(text_data=json.dumps({
      "tester": tester
    }))