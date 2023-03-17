from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        error_messages={
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator': "Le mot de passe est trop similaire au nom d'utilisateur."
        }
    )
    password2 = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=(''),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        labels = {
            'username': 'Identifiant',
            'first_name': "Nom",
            'last_name': 'Prénon',
            'email': 'Adresse Mail',
        }
        help_texts = {
            'username': 'Utilisé pour se connecter',
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Identifiant")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")
