from django import forms
from django.forms import ModelForm
from blog.models import Ticket


class AddTicketsForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image',]

