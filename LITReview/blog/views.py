# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from blog.models import Ticket, Review, UserFollows
from blog.forms import AddTicketsForm, AddCritiqueForm, FollowForm
from django.db import IntegrityError
from itertools import chain

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def home(request):
    reviews_users_followers_list = []

    reviews = Review.objects.filter(user_id=request.user.id)
    tickets = Ticket.objects.filter(user_id=request.user.id)

    list_users_followed = UserFollows.objects.filter(user=request.user)
    list_users_followers = UserFollows.objects.filter(followed_user_id=request.user)

    if list_users_followed is not None:
        for user_followed in list_users_followed:
            reviews_users_followed = Review.objects.filter(user_id=user_followed.followed_user.id)
            tickets_users_followed = Ticket.objects.filter(user_id=user_followed.followed_user.id)
            if reviews_users_followed is not None:
                reviews = (reviews | reviews_users_followed)
            if tickets_users_followed is not None:
                tickets = (tickets | tickets_users_followed)

    if list_users_followers is not None:
        for user_followers in list_users_followers:
            reviews_users_followers = Review.objects.filter(user_id=user_followers.user.id)
            if reviews_users_followers is not None:
                for review_user in reviews_users_followers:
                    reviews_users_followers_list.append(review_user.ticket.id)
                for ticket in tickets:
                    if ticket.id in reviews_users_followers_list:
                        review_user = Review.objects.filter(
                            ticket_id=ticket.id,
                            user_id=user_followers.user.id
                        )
                        reviews = (reviews | review_user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'blog/home.html', context={'posts': posts, 'stars': range(1, 5+1)})

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def post(request):
    reviews = Review.objects.filter(user_id=request.user.id)
    tickets = Ticket.objects.filter(user_id=request.user.id)
    return render(request, "blog/post.html", context={'reviews': reviews, 'tickets': tickets, 'stars': range(1, 5+1)})

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def creatreview(request, pk):
    ticket = Ticket.objects.get(id=pk)
    if request.method == "POST":
        review_form = AddCritiqueForm(request.POST)
        if review_form.is_valid():
            review_form.save(request.user.id, ticket=ticket)
        return redirect("home")
    else:
        review_form = AddCritiqueForm()
    context = {'ticket': ticket, 'review_form': review_form}
    return render(request, 'blog/creatreview.html', context=context)

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def deletepost(request, pk):
    userpostTodel = Review.objects.get(id=pk, user_id=request.user.id)
    userpostTodel.delete()
    return redirect("post")

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def deleteticket(request, pk):
    userpostTodel = Ticket.objects.get(id=pk, user_id=request.user.id)
    userpostTodel.delete()
    return redirect("post")

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def modifiepost(request, pk, id_post):
    post_to_modify = Review.objects.get(id=pk, user_id=request.user.id)
    tickets = Ticket.objects.get(id=id_post)
    if request.method == "GET":
        review_form = AddCritiqueForm(instance=post_to_modify)
        return render(
            request=request,
            template_name="blog/modifiepost.html",
            context={"review_form": review_form, "tickets": tickets})
    elif request.method == "POST":
        ticket_form = AddCritiqueForm(request.POST, request.FILES, initial={
            "id": post_to_modify.id,
            "rating": post_to_modify.rating,
            "headline": post_to_modify.headline,
            "body": post_to_modify.body})
        if ticket_form.is_valid():
            post_to_modify.rating = ticket_form.cleaned_data.get("rating")
            post_to_modify.headline = ticket_form.cleaned_data.get("headline")
            post_to_modify.body = ticket_form.cleaned_data.get("body")
            post_to_modify.ticket_id = id_post
            post_to_modify.save()
        return redirect("post")

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def modifieticket(request, pk):
    post_to_modify = Ticket.objects.get(id=pk)
    tickets = Ticket.objects.filter(user_id=request.user.id, id=pk)
    if request.method == "GET":

        ticket_form = AddTicketsForm(instance=post_to_modify)
        return render(
            request=request,
            template_name="blog/modifieticket.html",
            context={"ticket_form": ticket_form, "tickets": tickets})
    elif request.method == "POST":
        ticket_form = AddTicketsForm(request.POST, request.FILES, initial={
            "id": post_to_modify.id,
            "title": post_to_modify.title,
            "description": post_to_modify.description,
            "image": post_to_modify.image})
        if ticket_form.is_valid():
            post_to_modify.title = ticket_form.cleaned_data.get("title")
            post_to_modify.description = ticket_form.cleaned_data.get("description")
            post_to_modify.image = ticket_form.cleaned_data.get("image")
            post_to_modify.save()
        return redirect("post")

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def abonnements(request):
    error = ""
    form = FollowForm()
    userfllows = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user_id=request.user)
    context = {
        'userfllows': userfllows,
        "followers": followers,
        "form": form,
        "error": error
    }
    if request.method == "POST":
        user_form = FollowForm(request.POST)
        if user_form.is_valid():
            find_user = user_form.cleaned_data.get("username")
            if find_user == request.user.username:
                error = f"{find_user} Vous ne pouvez pas vous suivre vous-même "
                context.update({"error": error})
                return render(request, 'blog/abonnements.html', context=context)
            else:
                try:
                    found_user = User.objects.get(username=find_user)
                except User.DoesNotExist:
                    error = f"{find_user} n'existe pas ! "
                    context.update({"error": error})
                    return render(request, 'blog/abonnements.html', context=context)
                try:
                    instance = UserFollows(user=request.user, followed_user=found_user)
                    instance.save()
                    followers = UserFollows.objects.filter(followed_user_id=request.user)
                    context.update({"followers": followers})
                    return redirect("abonnements")

                except IntegrityError:
                    error = f"Vous avez déjà suivi {find_user}"
                    context.update({"error": error})
                    return render(request, 'blog/abonnements.html', context=context)
    return render(request, 'blog/abonnements.html', context=context)

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def desabonnement(request, pk):
    userTodel = User.objects.get(username=pk)
    userFollowstoDel = UserFollows.objects.get(followed_user_id=userTodel.id, user_id=request.user.id)
    userFollowstoDel.delete()
    return redirect("abonnements")

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def add_critique(request):
    ticket_form = AddTicketsForm()
    review_form = AddCritiqueForm()
    if request.method == "POST":
        review_form = AddCritiqueForm(request.POST)
        ticket_form = AddTicketsForm(request.POST, request.FILES)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(request.user.id)
            review_form.save(request.user.id, ticket=ticket)
        return redirect("home")

    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'blog/add_critique.html', context=context)

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def add_tickets(request):
    if request.method == "POST":
        ticket_form = AddTicketsForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket_form.save(request.user.id)
            return redirect("home")
    else:
        ticket_form = AddTicketsForm()
    return render(request, "blog/add_tickets.html", context={"ticket_form": ticket_form})

# ---------------------------------------------------------------------------------------------------------------------#
