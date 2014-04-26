from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
import os

def get_image_path(instance, filename):
    return os.path.join('images', str(instance.id), filename)

def get_video_path(instance, filename):
    return os.path.join('videos', str(instance.id), filename)

def get_randfile_path(instance, filename):
    return os.path.join('randfile', str(instance.id), filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=500, blank=True, null=True)
    photo = models.FileField(upload_to=get_image_path, blank=True, null=True)
    video = models.FileField(upload_to=get_video_path, blank=True, null=True)
    rand_file = models.FileField(upload_to=get_randfile_path, blank=True, null=True)

    def photo_name(self):
        return os.path.basename(self.photo.name)

    def video_name(self):
        return os.path.basename(self.video.name)

    def __unicode__(self):
        return self.user.username

class UserFile(models.Model):
    file = models.FileField(upload_to=get_randfile_path, blank=True, null=True)
    profile = models.ForeignKey(UserProfile, unique=False)

    def file_name(self):
        return os.path.basename(self.file.name)

    def __unicode__(self):
        return self.profile.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)