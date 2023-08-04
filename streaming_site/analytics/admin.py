from django.contrib import admin
from .models import VideoCommentAnalytic, VideoLikeAnalytic, VideoViewAnalytic

# Register your models here.
admin.site.register(VideoCommentAnalytic)
admin.site.register(VideoLikeAnalytic)
admin.site.register(VideoViewAnalytic)