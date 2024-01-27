from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.CharField(max_length=50, null=True, default='no bio')
    image = models.ImageField(upload_to='media/static/images/image.png',
                              null=True, default='media/static/images/default.jpg')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    text = models.CharField(max_length=220, null=False)
    image = models.ImageField(upload_to='media/static/images/image.png',
                              null=True, default='media/static/images/default_image.jpg')
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Subscribe(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')


class Chat(models.Model):
    room_name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
