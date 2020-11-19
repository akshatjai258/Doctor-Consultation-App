  
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from .models import Post,BlogComment
from .forms import PostForm,UpdatePostForm,CommentForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .templatetags import extras
from django.urls import reverse_lazy, reverse
# Create your views here.
# def BlogHome(request):
#     return render(request,'blog/BlogHome.html',{})


class HomeView(ListView):
    model=Post
    template_name='blog/BlogHome.html'
    ordering=['-post_date']
    paginate_by=2


class ArticleDetailView(DetailView):
    model=Post
    template_name='blog/BlogDetail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()	
        context["total_likes"] = total_likes
        context['CommentForm'] = CommentForm
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["liked"] = liked
        return context

def ArticleDetail(request,pk):
    post=get_object_or_404(Post,id=pk)
    comments= BlogComment.objects.filter(post=post, parent=None).order_by('-id')
    
    total_likes = post.total_likes()
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():
            replyDict[reply.parent.id]=[reply]
        else:
            replyDict[reply.parent.id].append(reply)
    
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    if request.method == 'POST':
        parentSno= request.POST.get('parentSno')
        
        commentform =CommentForm(request.POST or None)
        if commentform.is_valid():
            if parentSno==None:
                comment=request.POST.get('comment')
                blogcomment=BlogComment.objects.create(post=post, user=request.user,comment=comment)
                blogcomment.save()
            else:
                parent= BlogComment.objects.get(id=parentSno)
                comment=request.POST.get('comment')
                blogcomment=BlogComment.objects.create(post=post, user=request.user,comment=comment,parent=parent)
                blogcomment.save()
                
                

            return HttpResponseRedirect((reverse('BlogDetail',kwargs={'pk':post.id})))
            
    else:
        commentform=CommentForm()
        
    context={
        'post':post,
        "total_likes" : total_likes,
        "CommentForm":commentform,
        "liked" : liked,
        'comments':comments,
        "replyDict" : replyDict
    }
    return render(request,'blog/BlogDetail.html',context)

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

def index_page(request,pk):
    logged_in_user = request.user
    logged_in_user_posts = Post.objects.filter(author=pk)
    paginated_list=Paginator(logged_in_user_posts,2)
    page_number=request.GET.get('page')
    doctor_page_obj=paginated_list.get_page(page_number)

    return render(request, 'index.html', {'posts': logged_in_user_posts,'doctor_page_obj':doctor_page_obj})

def LikeView(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	
	return HttpResponseRedirect(reverse('BlogDetail', args=[str(pk)]))