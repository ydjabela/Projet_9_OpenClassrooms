# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from blog.models import Ticket, Review, UserFollows
from blog.forms import AddTicketsForm, AddCritiqueForm, FollowForm, NewTicketForm, NewReviewForm
from django.db import IntegrityError

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def home(request):
    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = Review.objects.all()
    reviews = reviews.annotate(content_type=Value('TICKET', CharField()))
    return render(request, 'blog/home.html', context={'tickets': tickets, 'reviews': reviews})

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def post(request):
    reviews = Review.objects.filter(user_id=request.user.id)
    tickets = Ticket.objects.filter(user_id=request.user.id)
    return render(request, "blog/post.html", context={'reviews': reviews, 'tickets': tickets})

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
    post_to_modify = Review.objects.get(id=pk)
    tickets = Ticket.objects.get(id=id_post)
    print(pk, post_to_modify)
    if request.method == "GET":
        review_form = NewReviewForm(instance=post_to_modify)
        return render(
            request=request,
            template_name="blog/modifiepost.html",
            context={"review_form": review_form, "tickets": tickets})
    elif request.method == "POST":
        ticket_form = NewReviewForm(request.POST, request.FILES, initial={
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
    if request.method == "GET":
        ticket_form = NewTicketForm(instance=post_to_modify)
        return render(
            request=request,
            template_name="blog/modifieticket.html",
            context={"ticket_form": ticket_form})
    elif request.method == "POST":
        ticket_form = NewTicketForm(request.POST, request.FILES, initial={
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
    if request.method == "POST":
        ticket_form = AddTicketsForm(request.POST, request.FILES)
        review_form = AddCritiqueForm(request.POST)
        if review_form.is_valid() and ticket_form.is_valid:
            review_form.save(request.user.id)
            return redirect("post")
    else:
        review_form = AddCritiqueForm()
        ticket_form = AddTicketsForm()
    context = {'ticket_form': ticket_form, 'review_form': review_form}
    return render(request, 'blog/add_critique.html', context=context)

# ---------------------------------------------------------------------------------------------------------------------#


@login_required
def add_tickets(request):
    if request.method == "POST":
        ticket_form = AddTicketsForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket_form.save(request.user.id)
            return redirect("post")
    else:
        ticket_form = AddTicketsForm()
    return render(request, "blog/add_tickets.html", context={"ticket_form": ticket_form})

# ---------------------------------------------------------------------------------------------------------------------#
