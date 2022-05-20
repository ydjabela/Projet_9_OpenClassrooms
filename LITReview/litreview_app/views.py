from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from . import forms


def login(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            print(user)
            if user is not None:
                return redirect('home')
                # login(request, user)
                # message = f'Bonjour, {user.username}! Vous êtes connecté.'
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'litreview_app/login.html', context={'form': form, 'message': message})


def inscreption(request):
    print('jerefere')
    return render(request, 'litreview_app/inscreption.html')


def home(request):
    return render(request, 'litreview_app/home.html')
