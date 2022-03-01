from operator import mod
from re import template
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts,
        'title': 'Blog - Home'
    }
    return render(request,'myapp/home.html', context)

class PostListView(ListView):
    model = Post
    ordering = ['-date']
    paginate_by = 4
    template_name = 'myapp/home.html'  #app/model_viewtype.html
    context_object_name = 'posts'
    
class UserPostListView(ListView):
    model = Post
    ordering = ['-date']
    paginate_by = 4
    context_object_name = 'posts'
    template_name = 'myapp/user_posts.html'  #app/model_viewtype.html

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')
    
  

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'myapp/post_detail.html'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin,LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Post
    success_url="/"
 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def about(request):
    return render(request,'myapp/about.html',{'title': 'Blog - About'})