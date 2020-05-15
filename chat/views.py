from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Message
from django.contrib import messages

@login_required
def index(request):
    current_user=request.user
    users=User.objects.exclude(username=current_user).all()
    context={'users':users,'current_user':current_user}
    return render(request,'chat/index.html',context)

@login_required
def chat(request,user1,user2):
    return render(request,'chat/room.html',{'user1':user1,'user2':user2})


class MessageDeleteView(LoginRequiredMixin,DeleteView):
    model = Message
    success_url = '/chat/'
    template_name='chat/message_confirm_delete.html'
    def post(self, request, *args, **kwargs):
        self.to_delete = self.request.POST.get('todelete')
        if  self.to_delete:
            user1=self.request['kwargs']['user1']
            author=user1
            user2=self.request['kwargs']['user2']
            ar=[user1,user2]
            ar=sorted(ar)
            user1=ar[0]
            user2=ar[1]
            messages=Message.objects.filter(sort_str=f'{user1}_{user2}').all()
            if author == messages.first().author:
                messages.delete()
                messages.success(request,f'successfully deleted chat: of {user1} and {user2}')
                return redirect('chat-index')
        else:
            return self.get(self, *args, **kwargs)

@login_required
def message_delete(request,user1,user2):
    if request.method=='POST':
        to_delete = request.POST.get('todelete')
        if  to_delete:
            author=user1
            ar=[user1,user2]
            ar=sorted(ar)
            user1=ar[0]
            user2=ar[1]
            Message.objects.filter(sort_str=f'{user1}_{user2}').all().delete()
            messages.success(request,f'successfully deleted chat: of {user1} and {user2}')
            return redirect('chat-index')
    else:
        return render(request,'chat/message_confirm_delete.html')



