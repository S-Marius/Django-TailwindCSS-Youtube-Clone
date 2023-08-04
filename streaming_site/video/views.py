from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, render

from .models import Video, VideoComment, Playlist
from django.shortcuts import get_object_or_404
from .models import Video, VideoComment, VideoView

# Create your views here.
def video_post_view(request, slug):
    # Step 1: Retrieve the video using the slug
    video = get_object_or_404(Video, slug=slug)

    # Step 2: Get all the comments for the retrieved video
    comments = VideoComment.objects.filter(video=video)

    # Step 3: Get a simple recommendation list of the most viewed videos
    recommendation_list = Video.objects.filter(is_public=True).order_by('-view_counter')[:10]

    # Step 4: Create or update the VideoView object to increase the view count
    if request.user.is_authenticated:
        video_view, created = VideoView.objects.get_or_create(user=request.user, video=video)
        if created:
            # Increment the view_counter of the associated Video and CustomUser objects
            video.view_counter = F('view_counter') + 1
            video.uploader.view_counter = F('view_counter') + 1

            # Save both the video and the user objects
            video.save()
            video.uploader.save()

    # Step 5: Check if the user is subscribed to the video uploader's channel
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = request.user.subscriptions.filter(channel=video.uploader).exists()

    # Step 6: Handle video like/unlike functionality
    liked = False
    if request.user.is_authenticated:
        try:
            video_like = VideoLike.objects.get(user=request.user, video=video)
            liked = True
        except VideoLike.DoesNotExist:
            pass

    # Step 7: Handle video dislike/undislike functionality
    disliked = False
    if request.user.is_authenticated:
        try:
            video_dislike = VideoDislike.objects.get(user=request.user, video=video)
            disliked = True
        except VideoDislike.DoesNotExist:
            pass
            
    for comment in comments:
        if request.user.is_authenticated:
            comment.user_likes = VideoCommentLike.objects.filter(user=request.user, user_comment=comment).exists()
        else:
            comment.user_likes = False

    return render(request, 'video_post.html', {
        'video': video,
        'comments': comments,
        'recommendation_list': recommendation_list,
        'is_subscribed': is_subscribed,
        'liked': liked,
        'disliked': disliked,
        'comments': comments,
    })


from django.shortcuts import redirect, get_object_or_404
from .models import Video, VideoComment
from django.shortcuts import render, redirect

def add_video_comment_view(request, slug):
    # Step 1: Retrieve the video using the slug
    video = get_object_or_404(Video, slug=slug)

    # Step 2: Check if the user is authenticated
    if request.user.is_authenticated:
        # Step 3: Get the comment text from the request POST data
        comment_text = request.POST.get('comment_text', '')

        if comment_text.strip():  # Check if the comment is not empty or contains only whitespace
            # Step 4: Create the comment and link it to the video and authenticated user
            comment = VideoComment.objects.create(user=request.user, video=video, text=comment_text)
            video.comment_counter += 1
            video.save()

    # Step 5: Redirect the user back to the video post page
    return redirect('video_post', slug=slug)


from django.shortcuts import redirect
from core.models import *

def subscribe_view(request, slug):
    # Get the video based on the slug
    video = get_object_or_404(Video, slug=slug)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the uploader of the video
        uploader = video.uploader

        # Check if the user is not already subscribed to the uploader
        if not request.user.subscriptions.filter(channel=uploader).exists():
            # Create a Subscription object to establish the subscription
            subscription = Subscription(subscriber=request.user, channel=uploader)
            subscription.save()

            # Update the uploader's subscriber count
            uploader.subscriber_counter += 1
            uploader.save()

    # Redirect back to the video post page
    return redirect('video_post', slug=slug)

from django.shortcuts import get_object_or_404, redirect
from .models import Video, VideoLike

def unsubscribe_view(request, slug):
    # Step 1: Get the video using the slug
    video = get_object_or_404(Video, slug=slug)

    # Step 2: Get the authenticated user
    user = request.user

    # Step 3: Check if the user is subscribed to the video's uploader
    subscription = Subscription.objects.filter(subscriber=user, channel=video.uploader).first()

    # Step 4: If the user is subscribed, unsubscribe them
    if subscription:
        subscription.delete()

    # Step 5: Redirect the user back to the video page
    return redirect('video_post', slug=slug)

from django.http import JsonResponse

from django.shortcuts import redirect

from django.shortcuts import redirect, get_object_or_404
from .models import VideoComment, VideoCommentLike

from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import redirect, get_object_or_404

def like_unlike_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(VideoComment, id=comment_id)
        user = request.user

        try:
            comment_like = VideoCommentLike.objects.get(user=user, user_comment=comment)
            comment_like.delete()
            comment.like_counter -= 1
            comment.save()
        except VideoCommentLike.DoesNotExist:
            # Set the 'video' field when creating the VideoCommentLike object
            comment_like = VideoCommentLike.objects.create(user=user, user_comment=comment, video=comment.video)
            comment.like_counter += 1
            comment.save()

    return redirect('video_post', slug=comment.video.slug)





from .models import *

from django.shortcuts import redirect

def dislike_undislike_video(request, slug):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, slug=slug)
        user = request.user

        try:
            video_dislike = VideoDislike.objects.get(user=user, video=video)
            video_dislike.delete()
            video.dislike_counter -= 1
            video.save()
        except VideoDislike.DoesNotExist:
            video_dislike = VideoDislike.objects.create(user=user, video=video)
            video.dislike_counter += 1
            video.save()

    return redirect('video_post', slug=slug)


from django.shortcuts import redirect

def like_unlike_video(request, slug):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, slug=slug)
        user = request.user

        try:
            video_like = VideoLike.objects.get(user=user, video=video)
            video_like.delete()
            video.like_counter -= 1
            video.save()
        except VideoLike.DoesNotExist:
            video_like = VideoLike.objects.create(user=user, video=video)
            video.like_counter += 1
            video.save()

    return redirect('video_post', slug=slug)


def playlist_videos_view(request, slug):
    playlist = get_object_or_404(Playlist, slug=slug)

    return render(request, 'video_post.html', {'playlist': playlist})

def upload_video_view(request):
    return render(request, 'upload_video.html')