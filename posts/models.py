from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)

class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name='posts_from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='posts_to_user', on_delete=models.CASCADE)

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads', null=True)
    poster = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField('Approved', default=False)

    class Meta:
        ordering=['-created']

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)