from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Chat(models.Model):
    user1=models.ForeignKey(User,related_name='user1',on_delete=models.CASCADE)
    user2=models.ForeignKey(User,related_name='user2',on_delete=models.CASCADE)
    sort_str=models.CharField(max_length=100,default=f'{user1}_{user2}')
    content=models.TextField()
    timestamp=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.content} between {self.user1} and {self.user2}'

    def retrive_messages():
        return reversed(Chat.objects.order_by('-timestamp').all())

class Message(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    sort_str=models.CharField(max_length=100)
    content=models.TextField()
    timestamp=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.content} by {self.author} in {self.sort_str}'

    def retrive_messages():
        return reversed(Message.objects.order_by('-timestamp').all())

