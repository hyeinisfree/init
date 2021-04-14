from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages

from django.views.generic.edit import CreateView
from .forms import CreateUserForm, UpdateUserForm, ProfileForm, HomeworkUploadForm
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.decorators import login_required

from .models import InitUser, Profile, Homework, Homework_submit

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
      return redirect('update')
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
      return redirect('update')
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
      return redirect('get_profile')
  else:
    form = ProfileForm(instance=user.profile)
  return render(request, 'profile_update.html', {'form': form})

@login_required()
def homework(request):
  user = request.user
  if user.is_authenticated:
    user = InitUser.objects.get(username=user.username)
    return redirect('homework_list', user.year)
  return redirect('home')

@login_required()
def homework_list(request, year):
  user = request.user
  homeworks = Homework.objects.filter(year=year).order_by('-id')
  done = []
  for homework in homeworks:
    if Homework_submit.objects.filter(user_id=user.id, homework_id=homework.id).exists():
      done.append(True)
    else:
      done.append(False)
  submits = Homework_submit.objects.filter(user_id=user.id)
  return render(request, 'homework_list.html', {'homeworks': homeworks, 'done': done})

@login_required()
def homework_detail(request, year, homework_id):
  user = request.user
  homework = Homework.objects.get(id=homework_id)
  done = False
  if Homework_submit.objects.filter(user_id=user.id, homework_id=homework.id).exists():
    done = True
  return render(request, 'homework_detail.html', {'homework': homework, 'done': done})

@login_required()
def homework_submit(request, year, homework_id):
  homework = Homework.objects.get(id=homework_id)
  user = InitUser.objects.get(id=request.user.id)
  if Homework_submit.objects.filter(homework_id=homework.id, user_id=user.id).exists():
    return redirect('homework_update', year, homework_id)
  if request.method == "POST":
    form = HomeworkUploadForm(request.POST, request.FILES)

    if form.is_valid():
      submit = Homework_submit(homework_id=homework, user_id=user, contents=form.cleaned_data['contents'], file=form.cleaned_data['file'])
      submit.save()
      return redirect('homework_result', year, homework_id)
  else:
    form = HomeworkUploadForm()
  return render(request, 'homework_submit.html', {'form': form, 'homework': homework})

@login_required()
def homwork_update(request, year, homework_id):
  homework = Homework.objects.get(id=homework_id)
  user = InitUser.objects.get(id=request.user.id)
  if not Homework_submit.objects.filter(homework_id=homework.id, user_id=user.id).exists():
    return redirect('homework_submit', year, homework_id)
  submit = Homework_submit.objects.get(homework_id=homework_id, user_id=user)
  if request.method == "POST":
    form = HomeworkUploadForm(request.POST, request.FILES, instance=submit)

    if form.is_valid():
      print(form.cleaned_data)
      submit = form.save(commit=False)
      submit.save()
      return redirect('homework_result', year, homework_id)
  else:
    form = HomeworkUploadForm(instance=submit)
  return render(request, 'homework_update.html', {'form': form, 'homework': homework})

@login_required()
def homework_result(requerst, year, homework_id):
  return HttpResponse("homework result page")