from django import forms
from .models import users, Photo, PhotoLikes, Followers, PhotoTag
from django.contrib.auth.forms import UserCreationForm
import json, re
from urllib.request import urlopen
from random import randint
from django.db.models import F


class SighupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Username'}
    ), required=True, max_length=50)

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Email'}
    ), required=True, max_length=50)

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Password'}
    ), required=True, max_length=50)

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Conform Password'}
    ), required=True, max_length=50)

    class Meta:
        model = users
        fields = ['username', 'email', 'password1', 'password2']



class Ajax(forms.Form):
    args = []
    user = []

    def __init__(self, *args, **kwargs):

        self.args = args
        if len(args) > 1:
            self.user = args[1]
            if self.user.id == None:
                self.user = "NL"

    def error(self, message):
        return json.dumps({ "Status": "Error", "Message": message }, ensure_ascii=False)

    def success(self, message):
        return json.dumps({ "Status": "Success", "Message": message }, ensure_ascii=False)

    def items(self, json):
        return json

    def output(self):
        return self.validate()


class AjaxSavePhoto(Ajax):
    def validate(self):
        try:
            self.url = self.args[0]["url"]
            self.baseurl = self.args[0]["baseurl"]
            self.caption = self.args[0]["caption"]
        except Exception as e:
            return self.error("Malformed request, did not process.")

        if self.user == "NL":
            return self.error("Unauthorised request.")

        if len(self.caption) > 140:
                return self.error("Caption must be 140 characters.")

        if self.url[0:20] != "https://ucarecdn.com" or self.baseurl[0:20] != "https://ucarecdn.com":
            return self.error("Invalid image URL")

        result = urlopen(self.baseurl+"-/preview/-/main_colors/3/")
        data = result.read()
        data = json.loads(data.decode('utf-8'))

        main_colour = ""
        if data["main_colors"] != []:
            #main_colour = data["main_colors"][randint(0, 2)]
            for colour in data["main_colors"][randint(0, 2)]:
                main_colour = main_colour + str(colour) + ","
            main_colour = main_colour[:-1]

        result = urlopen(self.baseurl+"detect_faces/")
        data = result.read()
        data = json.loads(data.decode('utf-8'))

        tag_count = 0
        p = Photo(url=self.url, baseurl=self.baseurl, owner=self.user.username, likes=0, caption=self.caption, main_colour=main_colour)
        p.save()
        if data["faces"] != []:
            for face in data["faces"]:
                tag = PhotoTag(photoid=p.id, coords=face).save()
        tag_count = len(data["faces"])
        p.tags = tag_count
        p.save()

        return self.success("Image Uploaded")



class AjaxLikePhoto(Ajax):
    def validate(self):
        try:
            self.postid = self.args[0]["id"]
        except Exception as e:
            return self.error("Malformed request, did not process.")

        if self.user == "NL":
            return self.error("Unauthorised request.")

        if not PhotoLikes.objects.filter(liker=self.user.username, postid=self.postid).exists():
            Photo.objects.filter(id=self.postid).update(likes=F('likes')+1)
            like = PhotoLikes(postid=self.postid, liker=self.user.username)
            like.save()
        else:
            Photo.objects.filter(id=self.postid).update(likes=F('likes')-1)
            PhotoLikes.objects.filter(postid=self.postid, liker=self.user.username).delete()

        return self.success("Photo Liked!")

class AjaxPhotoFeed(Ajax):
    def validate(self):
        try:
            self.start = self.args[0]["start"]
        except Exception as e:
            return self.error("Malformed request, did not process.")
        out = []
        followerslist = [self.user.username]
        profilepics = {}

        for follower in Followers.objects.filter(follower=self.user.username):
            followerslist.append(follower.user)

        for user in users.objects.filter(username__in=followerslist):
            profilepics[user.username] = user.profilepic
            if user.profilepic == "":
                profilepics[user.username] = "static/assets/img/default.png"

        for item in Photo.objects.filter(owner__in=followerslist).order_by('-date_uploaded')[int(self.start):int(self.start)+3]:
            if PhotoLikes.objects.filter(liker=self.user.username).filter(postid=item.id).exists():
                liked = True
            else:
                liked = False
            out.append({ "PostID": item.id, "URL": item.url, "Caption": item.caption, "Owner": item.owner, "Likes": item.likes, "DateUploaded": item.date_uploaded.strftime("%Y-%m-%d %H:%M:%S"), "Liked": liked, "ProfilePic": profilepics[item.owner]+"", "MainColour": item.main_colour })

        return self.items(json.dumps(out))

class AjaxProfileFeed(Ajax):
    def validate(self):
        try:
            self.username = self.args[0]["username"]
            self.start = self.args[0]["start"]
        except Exception as e:
            return self.error("Malformed request, did not process.")
        out = []
        for item in Photo.objects.filter(owner=self.username).order_by('-date_uploaded')[int(self.start):int(self.start)+3]:
            if PhotoLikes.objects.filter(liker=self.user.username).filter(postid=item.id).exists():
                liked = True
            else:
                liked = False
            out.append({ "PostID": item.id, "URL": item.url, "Caption": item.caption, "Owner": item.owner, "Likes": item.likes, "DateUploaded": item.date_uploaded.strftime("%Y-%m-%d %H:%M:%S"), "Liked": liked, "MainColour": item.main_colour })

        return self.items(json.dumps(out))


class AjaxSetProfilePic(Ajax):
    def validate(self):
        try:
            self.url = self.args[0]["url"]
            self.baseurl = self.args[0]["baseurl"]
        except Exception as e:
            return self.error("Malformed request, did not process.")

        if self.user == "NL":
            return self.error("Unauthorised request.")

        if self.url[0:20] != "https://ucarecdn.com" or self.baseurl[0:20] != "https://ucarecdn.com":
            return self.error("Invalid image URL")

        u = users.objects.filter(username=self.user.username)[0]
        u.profilepic=self.url
        u.save()

        return self.success("Profile Image Uploaded")

class AjaxFollow(Ajax):
    def validate(self):
        try:
            self.follower = self.args[0]["user"]
        except Exception as e:
            return self.error("Malformed request, did not process.")

        if self.user == "NL":
            return self.error("Unauthorised request.")

        if self.user.username == self.follower:
                return self.error("Can't follow yourself")

        if not Followers.objects.filter(user=self.follower,follower=self.user.username).exists():
            f = Followers(user=self.follower, follower=self.user.username).save()
            following = True
        else:
            Followers.objects.filter(user=self.follower, follower=self.user.username).delete()
            following = False
        out = { "Following": following }
        return self.items(json.dumps(out))

class AjaxTagPhoto(Ajax):
    def validate(self):
        try:
            self.follower = self.args[0]["user"]
        except Exception as e:
            return self.error("Malformed request, did not process.")
