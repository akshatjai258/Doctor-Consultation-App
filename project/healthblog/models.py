from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=255)
    tag=models.CharField(max_length=255,null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    post_date=models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title + " " + str(self.author)

    def get_absolute_url(self):
        return reverse('BlogDetail',args=str(self.id))