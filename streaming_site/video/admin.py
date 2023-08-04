from django.contrib import admin
from .models import Video, VideoComment, VideoCommentLike, VideoCommentDislike, VideoLike, VideoDislike, VideoView, Playlist, PlaylistItem

# Register your models here.
admin.site.register(Video)
admin.site.register(VideoView)
admin.site.register(VideoLike)
admin.site.register(VideoDislike)
admin.site.register(VideoComment)
admin.site.register(VideoCommentLike)
admin.site.register(VideoCommentDislike)
admin.site.register(Playlist)
admin.site.register(PlaylistItem)