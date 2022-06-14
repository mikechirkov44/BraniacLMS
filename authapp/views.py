#from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView
from authapp.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from authapp.forms import CustomUserChangeForm, CustomUserCreationForm
from authapp.models import User
# Create your views here.
class CustomLoginView(LoginView):
    template_name = "authapp/login.html"
    extra_context = {
        'title' : 'Вход пользователя'
    }

class RegisterView(CreateView): 
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainapp:main_page')
    # template_name = 'authapp/register.html'


class CustomLogoutView(LogoutView):
    pass

class EditView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'authapp/edit.html'

    def get_object(self, queryset=None):
        return self.request.user


    def get_success_url(self) -> str:
        return reverse_lazy('authaapp:edit', args=[self.request.user.pk])
    
