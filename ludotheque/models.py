# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import gettext_lazy as _

class Auteurs(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    age = models.IntegerField(blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True, db_comment="URL de la photo de l'auteur")


class Categories(models.Model):
    nom = models.CharField(max_length=100)
    descriptif = models.TextField(blank=True, null=True, db_comment='Description de la catégorie')

    def __str__(self):
        chaine = f"Catégorie {self.nom}: \n{self.descriptif}"
        return chaine

class Commentaires(models.Model):
    jeu = models.ForeignKey('Jeux', models.CASCADE)
    joueur = models.ForeignKey('Joueurs', models.CASCADE)
    note = models.IntegerField(db_comment='Note entre 1 et 5')
    contenu = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)


class Jeux(models.Model):
    titre = models.CharField(max_length=200)
    annee_sortie = models.IntegerField(blank=True, null=True)
    photo_boite = models.URLField(max_length=255, blank=True, null=True, db_comment='URL de la photo de la boîte')
    editeur = models.CharField(max_length=100, blank=True, null=True)
    categorie = models.ForeignKey(Categories, models.DO_NOTHING)
    auteur = models.ForeignKey(Auteurs, models.DO_NOTHING)

    def __str__(self):
        chaine = f"Le jeux {self.titre} est sortie en {self.annee_sortie} et fu créer par {self.auteur} et publié par {self.editeur}"
        return chaine

class Joueurs(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)
    type = models.CharField(max_length=13, choices=[('professionnel', 'Professionnel'), ('particulier', 'Particulier')], default='particulier')


    def __str__(self):
        chaine = f"Le joueur {self.nom} {self.prenom} est un joueur de type {self.type}, son email est {self.email}"
        return chaine

class ListeJeux(models.Model):
    joueur = models.ForeignKey(Joueurs, models.DO_NOTHING)
    jeu = models.ForeignKey(Jeux, models.DO_NOTHING)
    date_ajout = models.DateTimeField(auto_now_add=True)

