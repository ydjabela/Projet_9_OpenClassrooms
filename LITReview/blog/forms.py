from django import forms
from blog.models import Ticket, Review, UserFollows
from django.forms import ModelForm
from django.forms.widgets import TextInput

# ---------------------------------------------------------------------------------------------------------------------#


class AddTicketsForm(ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "image"
            ]
    title = forms.CharField(label='Titre')
    description = forms.CharField(label='Description')
    description.widget.attrs.update({'class': 'description_class'})
    image = forms.ImageField(label='Image')

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
            "headline",
            "rating",
            "body"
            ]

    headline = forms.CharField(label='Titre')
    body = forms.CharField(label='Commentaire')
    body.widget.attrs.update({'class': 'description_class'})
    RATINGS = [("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]
    rating = forms.ChoiceField(label='Note', widget=forms.RadioSelect, choices=RATINGS)
    rating.widget.attrs.update({'class': 'rating_class'})

    def save(self, user_id, ticket, commit=True,):
        review = super(AddCritiqueForm, self).save(commit=False)
        review.user_id = user_id
        review.ticket = ticket
        if commit:
            review.save()
        return review

# ---------------------------------------------------------------------------------------------------------------------#


class FollowForm(forms.Form):
    username = forms.CharField(label="", widget=TextInput({"placeholder": "Username", "class": "form-title"}))

# ---------------------------------------------------------------------------------------------------------------------#


