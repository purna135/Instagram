from django.shortcuts import render, HttpResponseRedirect
from .forms import *
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username= username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.warning(request, 'Username and password did not matched')
        except:
            pass
    return render(request, 'login.html')


def signup(request):
    form = SighupForm()
    if request.method == 'POST':
        form = SighupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup Successful. Please Login Here')
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'sign-up.html', {'form': form})


def home(request):
    context={}
    if request.user.is_authenticated:
        u = users.objects.get(username=request.user.username)
        if u.profilepic == "":
            u.profilepic = "static/assets/img/default.png"
        context = { 'user': request.user, 'ProfilePic': u.profilepic}
        return render(request, 'home.html', context)
    return HttpResponseRedirect(reverse('login'))


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def ajaxsavephoto(request):
    ajax = AjaxSavePhoto(request.POST, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)


def ajaxphotofeed(request):
    ajax = AjaxPhotoFeed(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)

def ajaxlikephoto(request):
    ajax = AjaxLikePhoto(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)

def ajaxtag(request):
    ajax = AjaxTagPhoto(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)

def ajaxfollow(request):
    ajax = AjaxFollow(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)

def ajaxsetprofilepic(request):
    ajax = AjaxSetProfilePic(request.POST, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)


def ajaxprofilefeed(request):
    ajax = AjaxProfileFeed(request.GET, request.user)
    context = { 'ajax_output': ajax.output() }
    return render(request, 'ajax.html', context)


def profile(request, username):
    if not users.objects.filter(username=username).exists():
        return HttpResponseRedirect(reverse('login'))
    u = users.objects.filter(username=username)[0]
    following = (
        "Unfollow"
        if Followers.objects.filter(
            user=username, follower=request.user.username
        ).exists()
        else "Follow"
    )

    if u.profilepic == "":
        u.profilepic = "static/assets/img/default.png"
    context = { "ProfilePic": u.profilepic, "whosprofile": username, "logged_in_as": request.user.username, "following": following }
    if request.user.is_authenticated:
        return render(request, 'logged-in-profile.html', context)
    return render(request, 'profile.html', context)

# def upload(request):
#     form = UploadForm()
#     print(form.media)
#     return render(request, 'upload.html', { 'form': form })