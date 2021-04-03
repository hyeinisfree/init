from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'last_name', 'first_name', 'email', 'year']
        
class UpdateUserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'last_name', 'first_name', 'email', 'year']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img', 'nickname', 'birthday', 'bio', 'git']