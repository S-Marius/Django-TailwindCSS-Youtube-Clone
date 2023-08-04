from django.db import models
from video.models import Video

# Create your models here.
class VideoViewAnalytic(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    total_views = models.PositiveIntegerField(default=0)

class VideoLikeAnalytic(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    total_likes = models.PositiveIntegerField(default=0)

class VideoCommentAnalytic(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    total_comments = models.PositiveIntegerField(default=0)