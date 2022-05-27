import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from heartbeat_app.models import User, MeetingLog

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.meeting_name = self.scope['url_route']['kwargs']['meeting_name'] 
        self.room_group_name = 'chat_%s' % self.meeting_name 

        self.participants_ids = list(MeetingLog.objects.values('participantId').filter(meetingName = self.meeting_name).distinct())
        self.participants_list = []

        for id_obj in self.participants_ids:
            participant_id = id_obj.get('participantId')
            participant_name = User.objects.values('username').filter(id = participant_id)[0].get('username')
            self.participants_list.append(participant_name)

       
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': ''    #f"{self.participants_list}"
                # 'lista': f"{self.participants_list}"
            }
        )
        self.accept()  


    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    
    def chat_message(self, event):
        self.meeting_name = self.scope['url_route']['kwargs']['meeting_name']
        message = event['message']  
        
        self.send(text_data=json.dumps({    
            'message': message,
            'lista': f"{self.participants_list}"
        }))


    def receive(self, text_data):   
        load_user_input = json.loads(text_data)
        message = load_user_input['message']
        userId = load_user_input['userId']
        username = User.objects.values('username').filter(id = userId)[0].get('username')
        message = (username + ":" + message)
        
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'lista': f"{self.participants_list}"
            }
        )