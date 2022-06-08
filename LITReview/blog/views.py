# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.db.models import CharField, Value
from blog.models import Ticket, Review, UserFollows
from blog.forms import AddTicketsForm, AddCritiqueForm


@login_required
def home(request):
    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('TICKET', CharField()))
    return render(request, 'blog/home.html', context={'tickets': tickets, 'reviews': reviews})


@login_required
def post(request):
    list_posts = Review.objects.filter(user_id=request.user.id)
    return render(
        request,
        template_name="blog/post.html",
        context={
            'reviews': list_posts,
        })


@login_required
def abonnements(request):
    '''
    followedUsers = UserFollows.objects.filter(user=request.user)
    followedUserObj = []
    for e in followedUsers:
        id_user = e.followed_user_id
        followedUserObj.append(User.objects.get(id=id_user).username)
    context["followedUserObj"] = followedUserObj
    followers = UserFollows.objects.filter(followed_user_id=request.user)
    followersObj = []
    for e in followers:
        id_user = e.user_id
        followersObj.append(User.objects.get(id=id_user).username)
    context["followersObj"] = followersObj
    '''
    userfllows = UserFollows.objects.filter(user=request.user)
    # userfllows = userfllows.annotate(content_type=Value('UserFollows', CharField()))
    followers = UserFollows.objects.filter(followed_user_id=request.user)
    return render(request, 'blog/abonnements.html', context={'userfllows': userfllows, "followers": followers})


@login_required
def add_critique(request):
    if request.method == "POST":
        ticket_form = AddTicketsForm(request.POST, request.FILES)
        review_form = AddCritiqueForm(request.POST)
        if review_form.is_valid() and ticket_form.is_valid:
            review_form.save(request.user.id)
            return redirect("add_critique")
    else:
        review_form = AddCritiqueForm()
        ticket_form = AddTicketsForm()
    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'blog/add_critique.html', context=context)


@login_required
def add_tickets(request):
    if request.method == "POST":
        ticket_form = AddTicketsForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket_form.save(request.user.id)
            return redirect("add_tickets")
    else:
        ticket_form = AddTicketsForm()

    return render(request, "blog/add_tickets.html", context={"ticket_form": ticket_form})
