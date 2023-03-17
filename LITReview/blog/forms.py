from django import forms

from blog.models import Ticket


class CreationTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Titre du livre',
            'description': "Description",
            'image': 'Image du livre',
        }
