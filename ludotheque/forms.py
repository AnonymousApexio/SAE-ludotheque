from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import *


class AuteurForm(ModelForm):
    class Meta:
        model = Auteurs
        fields = ('nom', 'prenom', 'age', 'photo')
        labels = {
            'nom': _('Nom'),
            'prenom': _('Prénom'),
            'age': _('Âge'),
            'photo': _('URL de la photo'),
        }
        help_texts = {
            'photo': _("URL complète de l'image de l'auteur")
        }


class CategorieForm(ModelForm):
    class Meta:
        model = Categories
        fields = ('nom', 'descriptif')
        labels = {
            'nom': _('Nom de la catégorie'),
            'descriptif': _('Description'),
        }
        widgets = {
            'descriptif': forms.Textarea(attrs={'rows': 4}),
        }


class JeuForm(ModelForm):
    class Meta:
        model = Jeux
        fields = ('titre', 'annee_sortie', 'photo_boite', 'editeur', 'categorie', 'auteur')
        labels = {
            'titre': _('Titre du jeu'),
            'annee_sortie': _('Année de sortie'),
            'photo_boite': _('URL de la photo'),
            'editeur': _('Éditeur'),
            'categorie': _('Catégorie'),
            'auteur': _('Auteur'),
        }
        help_texts = {
            'photo_boite': _("URL complète de l'image de la boîte")
        }
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Joueurs

class JoueurForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Joueurs
        fields = ('email', 'nom', 'prenom', 'type')
        labels = {
            'email': 'Adresse email',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'type': 'Type de joueur',
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hacher le mot de passe
        user.mot_de_passe = make_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CommentaireForm(ModelForm):
    class Meta:
        model = Commentaires
        fields = ('jeu', 'joueur', 'note', 'contenu')
        labels = {
            'jeu': _('Jeu'),
            'joueur': _('Joueur'),
            'note': _('Note (1-5)'),
            'contenu': _('Commentaire'),
        }
        widgets = {
            'note': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'contenu': forms.Textarea(attrs={'rows': 4}),
        }


class ListeJeuxForm(ModelForm):
    class Meta:
        model = ListeJeux
        fields = ('joueur', 'jeu')
        labels = {
            'joueur': _('Joueur'),
            'jeu': _('Jeu à ajouter'),
        }