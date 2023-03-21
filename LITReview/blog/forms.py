from django import forms

from blog.models import Ticket, Review


class CreationTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre du livre',
            'description': "Description",
            'image': 'Image du livre',
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
