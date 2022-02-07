from django.conf import settings
from django.db import models
from apps.utils.models import Timestamps


class Status(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Blog(Timestamps, models.Model):
    ''' All blog entries, for blog_content field be able to embed html code'''
    
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='blog_posts')
    post_blurb = models.TextField(max_length=255)
    content = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    blog_url = models.CharField(max_length=200)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

