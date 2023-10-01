# chat/consumers.py
import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Conversation
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope["user"])
        # # print(self.scope["sessionid"])
        # print(self.scope["session"])
        # print(self.scope["cookies"]["csrftoken"])
        # print("session id: " + self.scope["cookies"]["sessionid"])
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        # print("in recive message!!!")
        print(text_data)
        print(self.scope)

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]["message"]
        conversationId = text_data_json["message"]["conversationId"]
        print("message" + message)
        print("conversationId" + conversationId)
        sent_by = "Human"
        # save received message to db
        await self.save_message(message, sent_by, conversationId)

        # process Machine learning
        bot_response = f'Hello there.. You said - {message}'

        await self.send(text_data=json.dumps({
            'message': bot_response
        }))
        sent_by = "AI"
        await self.save_message(bot_response, sent_by, conversationId)

    @database_sync_to_async
    def save_message(self, text, sent_by, conversationId):
        message = Message()
        message.body = text
        message.sent_by = sent_by
        message.created_by = self.scope["user"]
        message.session_id = self.scope["cookies"]["sessionid"]
        conversation = Conversation.objects.get(pk=conversationId)
        message.conversationId = conversation

        headers = " ".join(str(x) for x in self.scope["headers"])
        message.context_data = {  # type: ignore
            'type': self.scope["type"],
            'headers': headers,
            'cookies': self.scope["cookies"],
        }
        message.save()
