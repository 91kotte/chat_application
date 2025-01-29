# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer  # A Django Channels class that helps handle WebSocket connections asynchronously.
from django.contrib.auth.models import User #Django’s built-in user model to manage user accounts
from .models import Message
from asgiref.sync import sync_to_async #Converts synchronous Django ORM queries into asynchronous calls.

# defines a Django Channels WebSocket consumer for handling chat messages asynchronously
class ChatConsumer(AsyncWebsocketConsumer):
    # WebSocket Connection Handling
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #Retrieves the room_name from the WebSocket URL.
        user1 = self.scope['user'].username  #Retrieves the currently logged-in user.
        user2 = self.room_name
        self.room_group_name = f"chat_{''.join(sorted([user1, user2]))}" #A unique chat group name is created by sorting both usernames (user1 and user2) and prefixing it with "chat_". This ensures a consistent group name regardless of who initiates the chat.

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name) #Adds the WebSocket connection to a Django Channels group for real-time communication.
        await self.accept() #Accepts the WebSocket connection

    # Removes the WebSocket connection from the chat group when the user leaves
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receiving Messages from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data) #Convert received JSON string to Python dictionary
        message = text_data_json['message'] #Extract message content
        sender = self.scope['user']  #Retrieve the sender (currently connected user)
        receiver = await self.get_receiver_user() #Get the receiver (other user in the chat room) asynchronously

        await self.save_message(sender, receiver, message) #Save message to the database

        # Broadcast the message to the chat group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', #The message is sent to all WebSocket connections in the chat group, triggering the chat_message method.
                'sender': sender.username,
                'receiver': receiver.username,
                'message': message
            }
        )
        
    # Handling Incoming Messages. This method is called when a message is broadcast in the group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']

        # Send message to the client via WebSocket.
        await self.send(text_data=json.dumps({
            'sender': sender,
            'receiver': receiver,
            'message': message
        }))

    # Stores the message in the database asynchronously using sync_to_async, ensuring that Django's ORM (which is synchronous) does not block the WebSocket.
    @sync_to_async
    def save_message(self, sender, receiver, message):
        Message.objects.create(sender=sender, receiver=receiver, content=message)

    # Retrieves the User object of the receiver (i.e., the chat partner) from the database.
    @sync_to_async
    def get_receiver_user(self):
        return User.objects.get(username=self.room_name)


