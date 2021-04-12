from django.contrib import admin
from .models import InitUser, Profile, Homework, Homework_submit
from django.contrib.auth.admin import UserAdmin

admin.site.register(InitUser)
admin.site.register(Profile)
admin.site.register(Homework)
admin.site.register(Homework_submit)