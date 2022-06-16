from django import forms
from django.forms import ModelForm
from blog.models import Ticket, Review, UserFollows
from django.forms import ModelForm
from django.conf import settings
from django.forms.widgets import ClearableFileInput, TextInput,Textarea,RadioSelect

# ---------------------------------------------------------------------------------------------------------------------#


class AddTicketsForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "image"
            ]

    def save(self, user_id, commit=True,):
        ticket = super(AddTicketsForm, self).save(commit=False)
        ticket.user_id = user_id
        if commit:
            ticket.save()
        return ticket

# ---------------------------------------------------------------------------------------------------------------------#


class AddCritiqueForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            "ticket",
            "rating",
            "headline",
            "body"
            ]

    def save(self, user_id, commit=True,):
        review = super(AddCritiqueForm, self).save(commit=False)
        review.user_id = user_id
        if commit:
            review.save()
        return review

# ---------------------------------------------------------------------------------------------------------------------#


class FollowForm(forms.Form):
    username = forms.CharField(label="", widget=TextInput({"placeholder": "Username", "class": "form-title"}))

# ---------------------------------------------------------------------------------------------------------------------#


class NewTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "image"
            ]

    def save(self, user_id, commit=True,):
        ticket = super(NewTicketForm, self).save(commit=False)
        ticket.user_id = user_id
        if commit:
            ticket.save()
        return ticket

# ---------------------------------------------------------------------------------------------------------------------#


class NewReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            "rating",
            "headline",
            "body"
            ]

    def save(self, user_id, commit=True,):
        review = super(NewReviewForm, self).save(commit=False)
        review.user_id = user_id
        if commit:
            review.save()
        return review
