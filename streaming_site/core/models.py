from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from imagekit.models import ProcessedImageField
from django.db.models import F
from imagekit.processors import ResizeToFill
from django.utils.text import slugify

# Create your models here.

class CustomUser(AbstractUser):
    avatar = ProcessedImageField(
        upload_to='user/avatars/',
        processors=[ResizeToFill(512, 512)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        default='user/avatars/default_avatar.jpg',
    )
    channel_banner = ProcessedImageField(
        upload_to='user/banners/',
        processors=[ResizeToFill(2560, 1440)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
        default='user/banners/default_banner.jpg',
    )
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20, blank=True, null=True, validators=[MinLengthValidator(3)])
    subscriber_counter = models.PositiveIntegerField(default=0)
    video_counter = models.PositiveIntegerField(default=0)
    view_counter = models.PositiveIntegerField(default=0)
    channel_description = models.TextField(blank=True, null=True, max_length=1000)
    country = models.CharField(max_length=100, blank=True, null=True, validators=[MinLengthValidator(2)])

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username

        super(CustomUser, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Check if the avatar path is different from the default path
        if self.avatar and self.avatar.path != 'user/avatars/default_avatar.jpg':
            self.avatar.delete()

        # Check if the channel banner path is different from the default path
        if self.channel_banner and self.channel_banner.path != 'user/banners/default_banner.jpg':
            self.channel_banner.delete()

        super(CustomUser, self).delete(*args, **kwargs)
        
    def __str__(self):
        return self.username
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscriptions")
    channel = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscribers")
    subscribe_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        CustomUser.objects.filter(pk=self.channel.pk).update(subscriber_counter=F('subscriber_counter') + 1)

        super(Subscription, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        CustomUser.objects.filter(pk=self.channel.pk).update(subscriber_counter=F('subscriber_counter') - 1)
        super(Subscription, self).delete(*args, **kwargs)

    def __str__(self):
        return f"'{self.subscriber.username}' subscribed to -> '{self.channel.username}'"