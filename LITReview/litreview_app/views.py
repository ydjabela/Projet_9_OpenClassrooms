from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . import forms


def logout_user(request):
    logout(request)
    return redirect('login')


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'

    return render(
        request, 'litreview_app/login.html', context={'form': form, 'message': message})


def inscription(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('login')

    return render(request, 'litreview_app/inscreption.html', context={'form': form})


@login_required
def home(request):
    return render(request, 'litreview_app/home.html')
