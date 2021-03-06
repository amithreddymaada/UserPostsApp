from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Posts
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse


# Create your views here.

def home(request):
    posts=Posts.objects.all()
    context={
        'posts':posts,
    }
    return render(request,'blog/home.html',context)

class PostsListView(LoginRequiredMixin,ListView):
    model = Posts
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostsListView(LoginRequiredMixin,ListView):
    model = Posts
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')

class PostsDetailView(LoginRequiredMixin,DetailView):
    model = Posts

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

class PostsCreateView(LoginRequiredMixin,CreateView):
    model = Posts
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author =self.request.user
        subject=f"New Post added by {self.request.user}"
        from_email=settings.EMAIL_HOST_USER
        to_email=[]
        for user in User.objects.all():
            to_email.append(user.email)
        contact_message = f"Title of Post:{form.instance.title}  Go and Check the post https://userpostsapp.herokuapp.com/"
        send_mail(subject,contact_message,from_email,to_email,fail_silently=True)
    
        return super().form_valid(form)

class PostsUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Posts
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author =self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostsDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
        model = Posts
        success_url ='/'
        def test_func(self):
            post = self.get_object()
            if self.request.user == post.author:
                return True
            return False

def about(request):
    return render(request,'blog/about.html',{})
