# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view, name='main_page'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('channel-edit/', views.channel_edit_view, name='channel_edit'),
    path('channel/<slug:username>/', views.channel_page_view, name='channel_page'),
    path('channel/<slug:username>/videos/', views.channel_page_videos_view, name='channel_page_videos'),
    path('channel/<slug:username>/playlists/', views.channel_page_playlists_view, name='channel_page_playlists'),
    path('channel/<slug:username>/playlist/<slug:playlist_url>/', views.playlist_view, name='playlist'),
    path('channel/<slug:username>/about/', views.channel_page_about_view, name='channel_page_about'),
    path('feed/subscriptions/', views.subscriptions_view, name='subscriptions'),
    path('feed/history/', views.history_view, name='history'),
    path('feed/liked/', views.liked_videos_view, name='liked_videos'),
]