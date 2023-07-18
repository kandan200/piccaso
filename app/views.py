from decimal import Decimal
from django.urls import reverse_lazy
import random
from django.shortcuts import render, redirect
# from .models import Client
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User
import bleach
from .forms import SignUpForm, SignInForm, PasswordResetRequestForm, PasswordResetConfirmForm, AccountActivationForm
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage, send_mail
from project import settings
from django.contrib.auth import authenticate, login
import requests


# Create your views here.
def home(request):
    return render(request, 'home.html', status=200)

def about(request):
    return render(request, 'about.html', status=200)

def contact_us(request):
    return render(request, 'contact_us.html', status=200)

def signin(request):
    form = SignInForm()
    return render(request, 'sign_in.html', {'form': form}, status=200)

def signup(request):
    form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form}, status=200)

def password_reset_confirm(request, uid, token):
    form = PasswordResetConfirmForm()
    form.uid =uid
    form.token = token
    return render(request, 'password_reset_confirm.html', {'form':form})

def logout(request):
    pass

def activation(request, uid, token):
    form = AccountActivationForm(data={'uid':uid, 'token':token})
    return render(request, 'activate.html', {'form':form})

def password_reset(request):
    form = PasswordResetRequestForm()
    return render(request, 'reset_password.html', {'form':form})