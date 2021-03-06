from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages

from django.views.generic.edit import CreateView
from .forms import CreateUserForm, UpdateUserForm, ProfileForm, HomeworkUploadForm
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.decorators import login_required

from .models import InitUser, Profile, Homework, Homework_submit, Notice

from django.core.mail.message import EmailMessage
from django.utils import timezone

from django.views.generic import ListView
from django.db.models import Q
from datetime import datetime

def send_email(request):
    subject = "message"
    to = ["kimhyein7110@gmail.com"]
    from_email = "kimhyein7110@gmail.com"
    message = "메지시 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

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
  time = timezone.now()
  done = False
  if Homework_submit.objects.filter(user_id=user.id, homework_id=homework.id).exists():
    done = True
  return render(request, 'homework_detail.html', {'homework': homework, 'done': done, 'time' : time})

@login_required()
def homework_submit(request, year, homework_id):
  homework = Homework.objects.get(id=homework_id)
  user = InitUser.objects.get(id=request.user.id)
  if Homework_submit.objects.filter(homework_id=homework.id, user_id=user.id).exists():
    return redirect('homework_update', year, homework_id)
  if request.method == "POST":
    form = HomeworkUploadForm(request.POST, request.FILES)

    if form.is_valid():
      submit = Homework_submit(homework_id=homework, user_id=user, contents=form.cleaned_data['contents'], file=form.cleaned_data['sfile'])
      submit.save()
      return redirect('homework_detail', year, homework_id)
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
      return redirect('homework_detail', year, homework_id)
  else:
    form = HomeworkUploadForm(instance=submit)
  return render(request, 'homework_update.html', {'form': form, 'homework': homework})

class NoticeListView(ListView):
  model = Notice
  paginate_by = 10
  template_name = 'notice_list.html'
  context_object_name = 'notice_list'

  def get_queryset(self):
    search_keyword = self.request.GET.get('q', '')
    search_type = self.request.GET.get('type', '')
    notice_list = Notice.objects.order_by('-id') 
    
    if search_keyword :
      if len(search_keyword) > 1 :
        if search_type == 'all':
          search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (contents__icontains=search_keyword) | Q (writer__username__icontains=search_keyword))
        elif search_type == 'title_contents':
          search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (contents__icontains=search_keyword))
        elif search_type == 'title':
          search_notice_list = notice_list.filter(title__icontains=search_keyword)    
        elif search_type == 'contents':
          search_notice_list = notice_list.filter(contents__icontains=search_keyword)    
        elif search_type == 'writer':
          search_notice_list = notice_list.filter(writer__username__icontains=search_keyword)

        return search_notice_list
    else:
      messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
    return notice_list

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    paginator = context['paginator']
    page_numbers_range = 5
    max_index = len(paginator.page_range)

    page = self.request.GET.get('page')
    current_page = int(page) if page else 1

    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    if end_index >= max_index:
      end_index = max_index

    page_range = paginator.page_range[start_index:end_index]
    context['page_range'] = page_range

    search_keyword = self.request.GET.get('q', '')
    search_type = self.request.GET.get('type', '')
    notice_fixed = Notice.objects.filter(top_fixed=True).order_by('-created_at')

    if len(search_keyword) > 1 :
      context['q'] = search_keyword
    context['type'] = search_type
    context['notice_fixed'] = notice_fixed

    return context

def notice_detail(request, notice_id):
  notice = Notice.objects.get(id=notice_id)
  return render(request, 'notice_detail.html', { 'notice' : notice})