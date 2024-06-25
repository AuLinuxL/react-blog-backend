from django.db import models
from django.contrib.auth.models import User
import os

def get_cover_path(instance, filename):
    ext = filename.split('.')[-1]
    name = f'post_cover_{str(instance.title)}.{ext}'
    return os.path.join('covers',name)

class Post(models.Model):
    cover = models.ImageField(upload_to=get_cover_path,null=True,blank=True)
    # title = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100)
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
    tags = models.ManyToManyField('Tag',blank=True)

class Tag(models.Model):
    # id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=50)

class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,default='')
    site = models.CharField(max_length=100,default='',blank=True)

# class UserInfo(models.Model):
#     name = models.CharField(max_length=100)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)

