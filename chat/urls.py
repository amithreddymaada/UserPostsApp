from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='chat-index'),
    path('<str:user1>/<str:user2>/',views.chat,name='chat-user'),
    path('<str:user1>/<str:user2>/delete/',views.message_delete,name='chat-delete'),
]