from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView
from .models import Post
from .forms import PostForm
# Create your views here.
# def BlogHome(request):
#     return render(request,'blog/BlogHome.html',{})


class HomeView(ListView):
    model=Post
    template_name='blog/BlogHome.html'


class ArticleDetailView(DetailView):
    model=Post
    template_name='blog/BlogDetail.html'

class AddPostView(CreateView):
    model=Post
    form_class=PostForm
    template_name='blog/AddBlog.html'
    
    

