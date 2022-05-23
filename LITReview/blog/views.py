# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'blog/home.html')
