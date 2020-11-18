from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.utils.timezone import now
from ckeditor.fields import RichTextField
# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=255)
    tag=models.CharField(max_length=255,null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    post_date=models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title + " " + str(self.author)

    def get_absolute_url(self):
        return reverse('BlogDetail',args=str(self.id))



class BlogComment(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)
    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
