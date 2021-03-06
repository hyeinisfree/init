"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import mysite.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mysite.views.home, name="home"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', mysite.views.CreateUserView.as_view(), name='signup'),
    path('update/', mysite.views.update, name='update'),
    path('password/', mysite.views.password, name='password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('profile/', mysite.views.get_profile, name='get_profile'),
    path('profile/update/', mysite.views.update_profile, name='update_profile'),

    path('homework/',mysite.views.homework, name="homework"),
    path('homework/<int:year>/', mysite.views.homework_list, name="homework_list"),
    path('homework/<int:year>/<int:homework_id>/', mysite.views.homework_detail, name='homework_detail'),
    path('homework/<int:year>/<int:homework_id>/submit/', mysite.views.homework_submit, name='homework_submit'),
    path('homework/<int:year>/<int:homework_id>/update/', mysite.views.homwork_update, name='homework_update'),

    path('notice/', mysite.views.NoticeListView.as_view(), name='notice_list'),
    path('notice/<int:notice_id>/', mysite.views.notice_detail, name='notice_detail')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
