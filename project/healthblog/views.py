from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from .models import Post
from .forms import PostForm,UpdatePostForm
from django.urls import reverse_lazy
# Create your views here.
# def BlogHome(request):
#     return render(request,'blog/BlogHome.html',{})


class HomeView(ListView):
    model=Post
    template_name='blog/BlogHome.html'
    ordering=['-post_date']


class ArticleDetailView(DetailView):
    model=Post
    template_name='blog/BlogDetail.html'

class AddPostView(CreateView):
    model=Post
    form_class=PostForm
    template_name='blog/AddBlog.html'

class UpdatePostView(UpdateView):
    model=Post
    form_class=UpdatePostForm
    template_name='blog/UpdatePost.html'
    # fields=['title','tag','body']
    
class DeletePostView(DeleteView):
    model=Post
    template_name='blog/DeletePost.html'
    success_url=reverse_lazy("BlogHome")

