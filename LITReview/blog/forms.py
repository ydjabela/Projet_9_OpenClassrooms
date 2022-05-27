from django import forms
from blog.models import Ticket, Review
from django.forms import ModelForm


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
