from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import CustomUser, Subscription
from video.models import Video, Playlist, PlaylistItem
from .forms import AvatarUploadForm, ChannelBannerUploadForm

# Create your views here.
def main_page_view(request):
    return render(request, 'home.html')

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if not (username and password and password_confirm):
            return render(request, 'register.html', {'error': 'Please provide both username and password.'})

        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        # Check if the username is already taken
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists. Please choose a different one.'})

        # Create the user object and set the password
        user = CustomUser.objects.create_user(username=username, password=password)

        # Authenticate the user and log them in
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_page')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def channel_page_view(request, username):
    video_list = Video.objects.filter(uploader__username=username)
    paginator = Paginator(video_list, 6)  # Show 6 videos per page

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)

    return render(request, 'user_page.html', {'videos': videos})


def upload_avatar_view(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    else:
        form = AvatarUploadForm(instance=request.user)
    return render(request, 'upload_avatar.html', {'form': form})

def upload_banner_view(request):
    if request.method == 'POST':
        form = ChannelBannerUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    else:
        form = ChannelBannerUploadForm(instance=request.user)
    return render(request, 'upload_banner.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from core.models import CustomUser

def channel_page_videos_view(request, username):
    video_list = Video.objects.filter(uploader__username=username)
    return render(request, 'user_page_videos.html', {'video_list': video_list})

from django.shortcuts import render

def channel_page_playlists_view(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        playlists = Playlist.objects.filter(user=user)
    except CustomUser.DoesNotExist:
        playlists = []

    playlist_data = []
    for playlist in playlists:
        try:
            first_video = playlist.playlistitem_set.first().video
        except PlaylistItem.DoesNotExist:
            first_video = None

        playlist_data.append({
            'playlist': playlist,
            'first_video': first_video,
        })

    return render(request, 'user_page_playlists.html', {'playlist_data': playlist_data})



def channel_page_about_view(request, username):
    video_list = Video.objects.filter(uploader__username=username)
    return render(request, 'user_page_about.html', {'video_list': video_list})
