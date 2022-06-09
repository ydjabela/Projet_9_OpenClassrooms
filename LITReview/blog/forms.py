from django import forms
from blog.models import Ticket, Review, UserFollows
from django.forms import ModelForm
from django.conf import settings


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


class UserForm(forms.Form):
    """
        A class to represent a form for a Userfollow
        Attributes
        ----------
        username :str
        email : str
        password1 : str
        password2 : str
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs["user"]
        del kwargs["user"]
        super().__init__(*args, **kwargs)
        self.fields["user_list"] = forms.ModelChoiceField(
            to_field_name="username",
            queryset=self.get_users_list())

    def get_users_list(self):
        fe = UserFollows.objects.filter(user=self.user)
        return (settings.AUTH_USER_MODEL.objects.all().order_by("username")
                .exclude(pk=self.user.id)
                .exclude(
                    pk__in=[settings.AUTH_USER_MODEL.objects.get(id=e.followed_user_id).id for e in fe]
                ))