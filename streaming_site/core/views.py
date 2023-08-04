from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import CustomUser, Subscription
from video.models import Video, Playlist, PlaylistItem

# Create your views here.
def main_page_view(request):
    most_viewed_videos = Video.objects.filter(is_public=True).order_by('-view_counter', '-upload_date')[:5]
    most_recent_videos = Video.objects.filter(is_public=True).order_by('-upload_date')[:5]

    user = request.user
    subscriptions = Subscription.objects.filter(subscriber=user)
    subscribed_channels = [subscription.channel for subscription in subscriptions]
    recent_videos_from_subscriptions = Video.objects.filter(uploader__in=subscribed_channels, is_public=True).order_by('-upload_date')[:5]

    return render(request, 'home.html', {'most_viewed_videos': most_viewed_videos, 'most_recent_videos': most_recent_videos, 'recent_videos_from_subscriptions': recent_videos_from_subscriptions})


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

# views.py
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from .models import CustomUser

def channel_edit_view(request):
    user = request.user

    if request.method == 'POST':
        # Update the user's information based on the form data
        avatar_file = request.FILES.get('avatar')
        channel_banner_file = request.FILES.get('channel_banner')

        if avatar_file:
            user.avatar = avatar_file
        if channel_banner_file:
            user.channel_banner = channel_banner_file

        user.channel_description = request.POST.get('channel_description')
        user.nickname = request.POST.get('nickname')
        user.country = request.POST.get('country')
        user.save()
        return redirect('main_page')

    return render(request, 'channel_edit.html', {'user': user})




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def channel_page_view(request, username):
    channel_page = get_object_or_404(CustomUser, username=username)
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

    return render(request, 'user_page.html', {'videos': videos, 'channel_page': channel_page, 'username': username})


from django.shortcuts import render, get_object_or_404
from core.models import CustomUser

def channel_page_videos_view(request, username):
    channel_page = get_object_or_404(CustomUser, username=username)
    video_list = Video.objects.filter(uploader__username=username)
    return render(request, 'user_page_videos.html', {'video_list': video_list, 'channel_page': channel_page, 'username': username})

from django.shortcuts import render

def channel_page_playlists_view(request, username):
    channel_page = get_object_or_404(CustomUser, username=username)
    try:
        user = CustomUser.objects.get(username=username)
        playlists = Playlist.objects.filter(user=user)
    except CustomUser.DoesNotExist:
        playlists = []

    playlist_data = []
    for playlist in playlists:
        first_video = None
        first_playlist_item = playlist.playlistitem_set.first()
        if first_playlist_item:
            first_video = first_playlist_item.video

        playlist_data.append({
            'playlist': playlist,
            'first_video': first_video,
        })

    return render(request, 'user_page_playlists.html', {'playlist_data': playlist_data, 'channel_page': channel_page, 'username': username})

from django.shortcuts import get_object_or_404

def playlist_view(request, username, playlist_url):
    channel_page = get_object_or_404(CustomUser, username=username)
    
    # Get the playlist based on the provided playlist_url
    playlist = get_object_or_404(Playlist, user__username=username, slug=playlist_url)

    # Get the videos related to the playlist
    videos = playlist.playlistitem_set.select_related('video').all()

    # Get the first video related to the playlist
    first_video_item = playlist.playlistitem_set.first()
    first_video = first_video_item.video if first_video_item else None
    
    return render(request, 'playlist.html', {'playlist': playlist, 'first_video': first_video, 'channel_page': channel_page, 'videos': videos,  'username': username})


def channel_page_about_view(request, username):
    channel_page = get_object_or_404(CustomUser, username=username)
    video_list = Video.objects.filter(uploader__username=username)
    return render(request, 'user_page_about.html', {'video_list': video_list, 'channel_page': channel_page, 'username': username})

from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from .models import CustomUser, Subscription
from video.models import Video

from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from .models import CustomUser, Subscription
from video.models import Video

def subscriptions_view(request):
    # Get the logged-in user's subscriptions
    logged_in_user = request.user
    subscriptions = Subscription.objects.filter(subscriber=logged_in_user)

    # Create an empty list to store videos from subscribed channels
    channel_videos = []

    # Loop through the subscriptions and get videos from each channel
    for subscription in subscriptions:
        channel = subscription.channel
        videos = Video.objects.filter(uploader=channel, upload_date__gte=timezone.now() - timedelta(days=7))
        channel_videos.extend(videos)

    # Sort the videos based on their upload_date in descending order
    channel_videos = sorted(channel_videos, key=lambda video: video.upload_date, reverse=True)

    return render(request, 'subscriptions.html', {'videos': channel_videos})

from django.shortcuts import render
from video.models import VideoView

def history_view(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get all the VideoView objects for the authenticated user and order them by the view_date
        history = VideoView.objects.filter(user=request.user).order_by('-view_date')
        return render(request, 'history.html', {'history': history})

    return render(request, 'history.html', {'history': []})  # Return an empty history list for non-authenticated users

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from video.models import Video, VideoLike

@login_required  # Require the user to be logged in to access this view
def liked_videos_view(request):
    # Step 1: Retrieve the VideoLike objects associated with the current user
    liked_videos = VideoLike.objects.filter(user=request.user)

    # Step 2: Extract the video IDs from the VideoLike objects
    liked_video_ids = liked_videos.values_list('video_id', flat=True)

    # Step 3: Fetch the Video objects based on the video IDs
    liked_videos_list = Video.objects.filter(id__in=liked_video_ids)

    return render(request, 'liked_videos.html', {'liked_videos_list': liked_videos_list})
