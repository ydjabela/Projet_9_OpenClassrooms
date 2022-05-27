from django import forms
from blog.models import Ticket
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

'''
class AddcCritiqueForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "ticket",
            "description",
            "image"
            ]

    def save(self, user_id, commit=True,):
        ticket = super(AddTicketsForm, self).save(commit=False)
        ticket.user_id = user_id
        if commit:
            ticket.save()
        return ticket

'''