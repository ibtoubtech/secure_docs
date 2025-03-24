from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """Formulaire personnalisé pour la création d'utilisateur"""
    first_name = forms.CharField(max_length=30, required=True)  # Prénom (obligatoire)
    last_name = forms.CharField(max_length=30, required=True)   # Nom (obligatoire)
    email = forms.EmailField(required=True)                     # Email (obligatoire)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        """Sauvegarde l'utilisateur avec les champs supplémentaires"""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
