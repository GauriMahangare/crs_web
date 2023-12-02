# chat/consumers.py
import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from intent.models import IntentExample
from .models import Message, Conversation
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]["message"]
        conversationId = text_data_json["message"]["conversationId"]
        sent_by = "Human"
        if message == 'quit':
            bot_response = f'Goodbye and Have a nice day {self.scope["user"].name}'
            await self.send(text_data=json.dumps({
                'message': bot_response
            }))
            sent_by = "AI"
            # save BOT message to db
            await self.save_message(bot_response, sent_by, conversationId)

            # Close the WebSocket connection for this client
            await self.close(code=1000,)
        else:
            # save received message to db
            await self.save_message(message, sent_by, conversationId)

            # process Machine learning
            #
            # Add model call here!!
            #
            await self.identifyIntent(message, sent_by, conversationId)

            bot_response = f'Hello there.. {self.scope["user"].name} said - {message}'

            await self.send(text_data=json.dumps({
                'message': bot_response
            }))
            sent_by = "AI"
            # save BOT message to db
            await self.save_message(bot_response, sent_by, conversationId)

    @database_sync_to_async
    def save_message(self, text, sent_by, conversationId):
        '''
        Function to save messages to database
        '''
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

    @database_sync_to_async
    def identifyIntent(self, text, sent_by, conversationId):
        '''
        Function to identify intents
        '''
        text = text.casefold()
        intent_examples_qs = IntentExample.objects.all()
        for example in intent_examples_qs:
            ex_text = example.example_text
