from django.db import models
from django.utils import timezone
import pytz
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp=models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.username
 
class blog(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='img',blank=True,null=True)
    content=models.TextField()
    published_date=models.DateTimeField(default=timezone.now,blank=True,null=True)
    l_add=models.IntegerField(default=0)
    dl_add=models.IntegerField(default=0,blank=True,null=True)
    
    
    # def __str__(self):
    #     return self.title
    
class trending_topics(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    published_date=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='img')
    path=models.URLField()
    
    
    def __str__(self):
        return self.title
    

class likes(models.Model):
    blog = models.ForeignKey(blog, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    reaction_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')], blank=True, null=True)
    like_dt = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Automatically adds the current timestamp

    class Meta:
        unique_together = ('blog', 'User')  # A user can like a specific blog only once

    
    
class comment(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    blog=models.ForeignKey(blog,on_delete=models.CASCADE,blank=True,null=True)
    
    message=models.TextField(blank=True,null=True)
    comment_date=models.DateTimeField(default=timezone.now,blank=True,null=True)
    
    def __str__(self):
        return self.message