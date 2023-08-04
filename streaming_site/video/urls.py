# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.video_post_view, name='video_post'),
    path('video/<slug:slug>/subscribe/', views.subscribe_view, name='subscribe'),
    path('<slug:slug>/', views.playlist_videos_view, name='playlist_videos'),
    path('upload-video/', views.upload_video_view, name='upload_video'),
    path('video/<slug:slug>/unsubscribe/', views.unsubscribe_view, name='unsubscribe'),
    path('video/<slug:slug>/add_comment/', views.add_video_comment_view, name='add_video_comment'),
    path('<slug:slug>/like/', views.like_unlike_video, name='like_unlike_video'),
    path('<slug:slug>/dislike/', views.dislike_undislike_video, name='dislike_undislike_video'),
    path('<slug:slug>/add_comment/', views.add_video_comment_view, name='add_video_comment'),
    path('video/comment/<int:comment_id>/like/', views.like_unlike_comment, name='like_unlike_comment'),
]