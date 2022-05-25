# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value
from blog.models import Ticket, Review
from . import forms


@login_required
def home(request):
    """
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    """
    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('TICKET', CharField()))
    return render(request, 'blog/home.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def post(request):

    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('TICKET', CharField()))
    return render(request, 'blog/post.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def abonnements(request):

    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('TICKET', CharField()))
    return render(request, 'blog/abonnements.html', context={'tickets': tickets, 'reviews': reviews})

@login_required
def add_critique(request):

    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('TICKET', CharField()))
    return render(request, 'blog/add_critique.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def add_tickets(request):
    ticket_form = forms.AddTicketsForm
    message = ''
    if request.method == 'POST':
        ticket_form = forms.AddTicketsForm(request.POST)
        if ticket_form.is_valid():
            tickets = authenticate(
                title=ticket_form.cleaned_data['title'],
            )
            if tickets is not None:
                # login(request, user)
                return redirect('add_tickets')
            else:
                message = 'Identifiants invalides.'

    return render(request, 'blog/add_tickets.html', context={'ticket_form': ticket_form})
