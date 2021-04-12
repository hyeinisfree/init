import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.db.models.signals import post_save
from django.core.files.storage import FileSystemStorage
from django import forms

class InitUser(AbstractUser):
  first_name = models.CharField(max_length=30, blank=False, null=False)
  last_name = models.CharField(max_length=150, blank=False, null=False)
  email = models.EmailField(blank=False, null=False, unique=True)
  year = models.CharField(max_length=20, null=False, blank=False)

# 파일들 overwrite 되게 하기
class OverwriteStorage(FileSystemStorage):
  def get_available_name(self, name, max_length=None):
    if(self.exists(name)):
      os.remove(os.path.join(settings.MEDIA_ROOT, name))
      return name

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
  img = ProcessedImageField(upload_to=profile_upload_to, storage=OverwriteStorage(), null=True, blank=True, processors=[Thumbnail(200,200),], format='JPEG', options={'quality':90,})
  birthday = models.DateField(null=True, blank=True)
  git = models.URLField(max_length=60, null=True, blank=True)

class Homework(models.Model):
  year = models.CharField(max_length=20, blank=False)
  title = models.CharField(max_length=200, blank=False)
  contents = models.TextField(blank=False)
  writer = models.ForeignKey(InitUser, on_delete=models.DO_NOTHING, db_column='writer')
  created_at  = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  end_date = models.DateTimeField(blank=False)

  def __str__(self):
    return self.title

# Homework_submit file 형식에 맞춰 업로드 되게 하기
def homework_upload_to(instance, filename):
  year = instance.homework_id.year
  writer = instance.homework_id.writer.username
  homework = instance.homework_id.title
  user = instance.user_id.username
  # 확장자 추출
  extension = os.path.splitext(filename)[-1].lower()
  # 결합 후 return
  return '/'.join([
    'homework_uploads',
    year,
    writer,
    homework + '_' +  user + extension,
  ])        

class Homework_submit(models.Model):
  homework_id = models.ForeignKey(Homework, on_delete=models.CASCADE, db_column='homework_id')
  user_id = models.ForeignKey(InitUser, on_delete=models.CASCADE, db_column='user_id')
  contents = models.TextField(blank=False)
  file = models.FileField(null=True, blank=True, upload_to=homework_upload_to, storage=OverwriteStorage())
  submitted_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.homework_id.title 