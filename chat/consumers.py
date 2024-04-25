import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, Message


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
    
    # method for connecting to the websocket
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']
        
        # add group_name to the channel layer
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        
        # accept websocket connection
        self.accept()
        
        # send user list to the client
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))
        
        if self.user.is_authenticated:
            # send message in group when user join
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            self.room.online.add(self.user)
    
    
    # method for disconnecting from the websocket
    def disconnect(self, close_code):
        # remove group_name instance from channel layer
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )
        
        if self.user.is_authenticated:
            # send message in group when user leave
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )
            self.room.online.remove(self.user)
        
    # method for receiving messages from the websocket
    def receive(self, text_data):
        # recieved text_data converted into dict
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        if not self.user.is_authenticated:
            return
        
        # send the event to the group  
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
            }
        )
        # create message instance
        Message.objects.create(user=self.user, room=self.room, content=message)
        
    # different data sent by group_send() method is sent to all active instance in same room
    def chat_message(self, event):
        # send the message to the websocket
        self.send(text_data=json.dumps(event))
        
    def user_join(self, event):
        # send message when user joins
        self.send(text_data=json.dumps(event))
        
    def user_leave(self, event):
        # send message when user leaves
        self.send(text_data=json.dumps(event))