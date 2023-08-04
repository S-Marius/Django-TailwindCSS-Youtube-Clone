from django.db import models
from django.core.validators import MinLengthValidator
from core.models import CustomUser
from django.db.models import F
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


import uuid

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=80, validators=[MinLengthValidator(5)])
    description = models.TextField(blank=False, max_length=1000, validators=[MinLengthValidator(5)])
    video_file = models.FileField(upload_to='videos/', blank=False, null=False)
    thumbnail = ProcessedImageField(
        upload_to='video_thumbnails/',
        processors=[ResizeToFill(1280, 720)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        default='video_thumbnails/default_video_thumbnail.jpg',
    )
    view_counter = models.PositiveIntegerField(default=0)
    like_counter = models.PositiveIntegerField(default=0)
    dislike_counter = models.PositiveIntegerField(default=0)
    comment_counter = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, editable=False)
    is_public = models.BooleanField(default=True)

    # Overwrite of the default save function
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is being created (not updated)
            if not self.slug:
                self.slug = str(uuid.uuid4())

            # Increase the video_counter on the uploader (CustomUser) model
            self.uploader.video_counter = F('video_counter') + 1
            self.uploader.save(update_fields=['video_counter'])

        super(Video, self).save(*args, **kwargs)

   
    def delete(self, *args, **kwargs):
        # Decrease the video_counter on the uploader (CustomUser) model
        self.uploader.video_counter = F('video_counter') - 1
        self.uploader.save(update_fields=['video_counter'])

        super(Video, self).delete(*args, **kwargs)

    
    def __str__(self):
        return self.title
        

class VideoView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    view_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        Video.objects.filter(pk=self.video.pk).update(view_counter=F('view_counter') + 1)

        super(VideoView, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Video.objects.filter(pk=self.video.pk).update(view_counter=F('view_counter') - 1)
        super(VideoView, self).delete(*args, **kwargs)
    
    def __str__(self):
        return f"'{self.user.username}' viwed the video '{self.video.title}'"    

class VideoLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        Video.objects.filter(pk=self.video.pk).update(like_counter=F('like_counter') + 1)

        super(VideoLike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Video.objects.filter(pk=self.video.pk).update(like_counter=F('like_counter') - 1)
        super(VideoLike, self).delete(*args, **kwargs)

    def __str__(self):
        return f"'{self.user.username}' liked the video '{self.video.title}'"    

class VideoDislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    dislike_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        Video.objects.filter(pk=self.video.pk).update(dislike_counter=F('dislike_counter') + 1)

        super(VideoDislike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Video.objects.filter(pk=self.video.pk).update(dislike_counter=F('dislike_counter') - 1)
        super(VideoDislike, self).delete(*args, **kwargs)

    def __str__(self):
        return f"'{self.user.username}' disliked the video '{self.video.title}'"     

class VideoComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    comment_date = models.DateTimeField(auto_now_add=True)
    like_counter = models.PositiveIntegerField(default=0)
    dislike_counter = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            Video.objects.filter(pk=self.video.pk).update(comment_counter=F('comment_counter') + 1)

        super(VideoComment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Video.objects.filter(pk=self.video.pk).update(comment_counter=F('comment_counter') - 1)
        super(VideoComment, self).delete(*args, **kwargs)

    def __str__(self):
        return f"'{self.user.username}' commented on '{self.video.title}'" 

    # @classmethod
    # def bulk_delete(cls, queryset):
    #     # Decrement like_counter when bulk deleting
    #     video_ids = queryset.values_list('video', flat=True)
    #     Video.objects.filter(pk__in=video_ids).update(like_counter=F('like_counter') - 1)

    #     # Call the superclass delete() method for bulk deletion
    #     super(VideoLike, cls).bulk_delete(queryset)
    
class VideoCommentLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(VideoComment, on_delete=models.CASCADE, related_name='comment_likes')
    like_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        VideoComment.objects.filter(pk=self.user_comment.pk).update(like_counter=F('like_counter') + 1)

        super(VideoCommentLike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        VideoComment.objects.filter(pk=self.user_comment.pk).update(like_counter=F('like_counter') - 1)
        super(VideoCommentLike, self).delete(*args, **kwargs)

    def __str__(self):
        return f"'{self.user.username}' liked comment of '{self.user_comment.user.username}' on '{self.video.title}'" 

class VideoCommentDislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(VideoComment, on_delete=models.CASCADE, related_name='comment_dislikes')
    dislike_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.user_comment.dislike_counter += 1
        self.user_comment.save()
        super(VideoCommentDislike, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user_comment.dislike_counter -= 1
        self.user_comment.save()
        super(VideoCommentDislike, self).delete(*args, **kwargs)

    def __str__(self):
        return f"'{self.user.username}' disliked comment of '{self.user_comment.user.username}' on '{self.video.title}'" 

class Playlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    description = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(unique=True, editable=False)
    video_counter = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically updated on save

    # Overwrite of the default save function
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())  # Generate a new UUID for the slug

        super(Playlist, self).save(*args, **kwargs) # First we are creating and adding the slug to itself if it doesn't exist, then we use the default save function provided by Django.
        
    def __str__(self):
        return f"'{self.name}' - '{self.user.username}'" 

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    # REMEMBER TO MAYBE ADD SLUG IN THE FUTURE FOR CURRENT VIDEO IN CURRENT PLAYLIST

    # Overwrite of the default save function
    def save(self, *args, **kwargs):
        super(PlaylistItem, self).save(*args, **kwargs)

        # Update the video_counter of the associated Playlist object
        Playlist.objects.filter(pk=self.playlist.pk).update(video_counter=F('video_counter') + 1)

    def delete(self, *args, **kwargs):
        playlist_pk = self.playlist.pk
        super(PlaylistItem, self).delete(*args, **kwargs)

        # Update the video_counter of the associated Playlist object
        Playlist.objects.filter(pk=playlist_pk).update(video_counter=F('video_counter') - 1)

    def __str__(self):
        return f"'{self.playlist.name}' - '{self.video.title}'"