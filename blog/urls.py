from django.contrib import admin
from django.urls import path,include
from . import views
from .views import (
    PostsListView,
    PostsDetailView,
    PostsCreateView,
    PostsUpdateView,
    PostsDeleteView,
    UserPostsListView

)

urlpatterns=[
    path('',PostsListView.as_view(),name='blog-home'),
    path('user/<str:username>/',UserPostsListView.as_view(),name='posts-user'),
    path('posts/<int:pk>/',PostsDetailView.as_view(),name='posts-detail'),
    path('posts/<int:pk>/update/',PostsUpdateView.as_view(),name='posts-update'),
    path('posts/create/',PostsCreateView.as_view(),name='posts-create'),
    path('posts/<int:pk>/delete/',PostsDeleteView.as_view(),name='posts-delete'),
    path('about/',views.about,name='blog-about'),
]