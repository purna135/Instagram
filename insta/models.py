from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class users(User):
    profilepic = models.CharField(max_length=255, default="")
    def __str__(self):
        return self.username


class Photo(models.Model):
    baseurl = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    date_uploaded = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=20)
    likes = models.IntegerField()
    caption = models.CharField(max_length=140, default="")
    tags = models.IntegerField(default=0)
    main_colour = models.CharField(max_length=15, default="")


class PhotoLikes(models.Model):
    postid = models.IntegerField()
    liker = models.CharField(max_length=20)


class Followers(models.Model):
    user = models.CharField(max_length=20, default="")
    follower = models.CharField(max_length=20, default="")


class PhotoTag(models.Model):
    photoid = models.IntegerField()
    coords = models.CharField(max_length=20)
    tagged_user = models.CharField(max_length=20, default="")
    tagged_by = models.CharField(max_length=20, default="")