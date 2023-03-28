from django import forms

from blog.models import Ticket, Review, UserFollows
from authentication.models import User


class CreationTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre du livre',
            'description': "Description",
            'image': 'Image du livre',
        }
        widgets = {
            "description": forms.Textarea()
        }


class CreationReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        choices=Review().RATING_SELECT,
        empty_value=None,
        widget=forms.RadioSelect())

    class Meta:
        model = Review
        fields = ('rating', "headline", "body",)
        labels = {
            'rating': 'Note',
            'headline': 'Titre',
            'body': 'Critique'
        }
        widgets = {
            "body": forms.Textarea()
        }


class UserFollowsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserFollowsForm, self).__init__(*args, **kwargs)

    def clean_subscription(self):
        data_subscription = self.cleaned_data['subscription']
        if str(data_subscription) == str(self.user):
            raise forms.ValidationError("Vous ne pouvez pas vous abonner a vous meme")
        elif not User.objects.filter(username=data_subscription).exists():
            raise forms.ValidationError("L'utilisateur n'existe pas")
        elif UserFollows.objects.filter(subscriber=self.user, subscription=data_subscription).exists():
            raise forms.ValidationError("Vous etes déja abonné a cet utilisateur")
        else:
            return data_subscription

    class Meta:
        model = UserFollows
        fields = ("subscription",)
        labels = {
            "subscription": "Ajouter un utilisateur",
        }
