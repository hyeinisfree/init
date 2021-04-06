import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.db.models.signals import post_save

class InitUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    year = models.CharField(max_length=20, null=False, blank=False)

# Profile image 형식에 맞춰 업로드 되게 하기
def profile_upload_to(instance, filename):
  user = instance.user.username
  # 확장자 추출
  extension = os.path.splitext(filename)[-1].lower()
  # 결합 후 return
  return '/'.join([
    'profile_uploads',
    user + extension,
  ])

# User 회원 가입 시 Profile 생성하기
def on_post_save_for_user(sender, **kwargs):
  if kwargs['created']:
    user = kwargs['instance']
    Profile.objects.create(user=user)

post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    img = ProcessedImageField(upload_to=profile_upload_to, null=True, blank=True, processors=[Thumbnail(200,200),], format='JPEG', options={'quality':90,})
    birthday = models.DateField(null=True, blank=True)
    git = models.URLField(max_length=60, null=True, blank=True)