from django.contrib import admin
from .models import InitUser, Profile
from django.contrib.auth.admin import UserAdmin

admin.site.register(InitUser)
admin.site.register(Profile)