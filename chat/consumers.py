import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
# from channels.db import database_sync_to_async
from .models import Message, Room, Information, RoomHistory
from django.contrib.auth.models import User


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_id = f'user'
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.user_group_id,
            self.channel_name
        )
        if self.scope['user'].is_authenticated:
            await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_id,
            self.channel_name
        )
        infors = await self.set_status(False,self.user_id)
        for info in infors:
            await self.channel_layer.group_send(
                f'user',
                {
                    'type':'user_status',
                    'user_id':info.user.id,
                    'status': info.status
                }
            )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        status = data.get('status')
        user_id = data.get('user_id')
        print(user_id)
        self.user_id = user_id
        if status == "WENT_ONLINE":
            infors = await self.set_status(True,user_id)
            for info in infors:
                await self.channel_layer.group_send(
                    f'user',
                    {
                        'type': 'user_status',
                        'user_id': info.user.id,
                        'status': info.status
                    }
                )
        elif status == "WENT_OFFLINE":
            infors = await self.set_status(False,user_id)
            for info in infors:
                await self.channel_layer.group_send(
                    f'user',
                    {
                        'type': 'user_status',
                        'user_id': info.user.id,
                        'status':  info.status
                    }
                )
            
    async def user_status(self,event):
        user_id = event['user_id']
        status = event['status']
        str = "OFFLINE"
        if status==True: str = "ONLINE"
        await self.send(text_data=json.dumps({
            'type_set':'USERS',
            'user_id':user_id,
            'status':str
        }))

    @sync_to_async
    def set_status(self, status, user_id):
        user = User.objects.get(id=user_id)
        Information.objects.filter(user=user).update(status=status)
        infors = Information.objects.all()
        return infors


class ChatConsumer(AsyncWebsocketConsumer):
    room_id = 0
    username = ""
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        self.username = data.get('username')
        self.room_id = data.get('room_id')
        type_set = data.get('type_set')
        # print(self.room_id)
        
        if type_set=="CHAT":
            date = await self.save_message(self.username, self.room_id, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.username,
                    'date': date
                }
            )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        date = event['date']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type_set':'CHAT',
            'message': message,
            'username': username,
            'date': date
        }))

    @sync_to_async
    def save_message(self, username, room_id, message):
        room = Room.objects.filter(id=room_id).first()
        user = User.objects.filter(username=username).first()
        message = Message.objects.create(user=user, room=room, content=message)
        return message.date_added.strftime("%d/%m/%Y %H:%M")