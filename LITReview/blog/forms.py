from blog.models import Ticket, Review, UserFollows
from django.forms import ModelForm, ImageField, CharField
from django.forms.widgets import TextInput, Textarea, RadioSelect

# ---------------------------------------------------------------------------------------------------------------------#


class AddTicketsForm(ModelForm, ImageField):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "image"
            ]
        widgets = {
            'title': TextInput(attrs={
                "placeholder": "Titre du livre",
                "class": "form-title"
            }),
            'description': Textarea(attrs={
                "placeholder": "Description du ticket",
                "class": "form-desc"}),
        }

    image = ImageField(label='Imaage')
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
        widgets = {
            'headline': TextInput(attrs={
                "placeholder": "Titre",
                "class": "form-title"
            }),
            'body': Textarea(attrs={
                "placeholder": "Commentaire",
                "class": "form-desc",
            }),
            'rating': RadioSelect(attrs={
                "class": "rating_class",
            }, choices=[("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]),
        }
        labels = {"headline": "Titre", "body": "Commentaire", "rating": "Note"}

    def save(self, user_id, ticket, commit=True,):
        review = super(AddCritiqueForm, self).save(commit=False)
        review.user_id = user_id
        review.ticket = ticket
        if commit:
            review.save()
        return review

# ---------------------------------------------------------------------------------------------------------------------#


class FollowForm(CharField):
    username = CharField(label="", widget=TextInput({"placeholder": "Username", "class": "form-title"}))

# ---------------------------------------------------------------------------------------------------------------------#


