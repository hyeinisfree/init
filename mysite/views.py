from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages

from django.views.generic.edit import CreateView
from .forms import CreateUserForm, UpdateUserForm, ProfileForm
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.decorators import login_required

def home(request):
  return render(request, 'index.html')

class CreateUserView(CreateView):
  template_name = 'signup.html'
  form_class =  CreateUserForm
  success_url = '/'

@login_required()
def update(request):
  user = request.user
  if request.method == 'POST':
      form = UpdateUserForm(request.POST, instance=user)
      if form.is_valid():
          form.save()
          return redirect('/')
  else:
    form = UpdateUserForm(instance = user)
  return render(request, 'update.html', {'form': form})

@login_required()
def password(request):
  user = request.user
  if request.method == 'POST':
      form = PasswordChangeForm(user, request.POST)
      if form.is_valid():
          s_user = form.save()
          update_session_auth_hash(request, s_user)
          return redirect('/')
  else:
      form = PasswordChangeForm(user)
  return render(request, 'password.html', {'form': form})

@login_required()
def get_profile(request):
  user = request.user
  return render(request, 'profile.html', {'user': user})

@login_required()
def update_profile(request):
  user = request.user
  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=user.profile)
    if form.is_valid():
      form.save()
      return redirect('/profile')
  else:
    form = ProfileForm(instance=user.profile)
  return render(request, 'profile_update.html', {'form': form})