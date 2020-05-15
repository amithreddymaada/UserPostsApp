import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Message
from django.contrib.auth.models import User
from django.utils import timezone

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['user1']
        self.user2 = self.scope['url_route']['kwargs']['user2']
        self.author=self.user1
        #to sort the two usernames and find the first one based upon we create a chat between that two users
        users=[self.user1,self.user2]
        users=sorted(users)

        self.user1=users[0]
        self.user2=users[1]

        self.room_name=f'{self.user1}_{self.user2}'
        self.room_group_name = f'chat_{self.user1}_{self.user2}'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self,data)

    def fetch_messages(self,data):
        messages=Message.retrive_messages()
        context = {
            'command':'messages',
            'messages':self.messages_to_json(messages)
        }
        self.send_messages(context)
        

    def new_messsage(self,data):
        msg_data=data
        # user=self.scope['user']
        # print(user.username)
        print('In new message')
        user=User.objects.get(username=self.author)
        message=Message.objects.create(author=user,sort_str=f'{self.user1}_{self.user2}',content=msg_data['message'])
        context={
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        self.send_chat_messages(context)

    commands={
        'fetch_messages':fetch_messages,
        'new_message':new_messsage
    }

    def messages_to_json(self,messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
    def message_to_json(self,message):
        return(
                {
                    'author':message.author.username,
                    'content':message.content,
                    'timestamp':str(message.timestamp)
                }
            )
    
    def send_messages(self,messages):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'previous_chats',
                'messages': messages
            }
        )
    def previous_chats(self,event):
        messages = event['messages']
        self.send(text_data=json.dumps(messages))

    def send_chat_messages(self,context):
        print('In send_chat_messages')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'context': context
            }
        )
        # print('at the end of send_chat_messages')
        # self.send(text_data=json.dumps({
        #     'message': context['message'],
        #     'command':context['command']
        # }))
        

    # Receive message from room group
    def chat_message(self, event):
        print('In chat_message')
        context = event['context']
        # print(context['message'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': context['message'],
            'command':context['command']
        }))
