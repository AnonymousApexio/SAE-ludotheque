from django.urls import path
from . import views

app_name = 'ludotheque'

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # ================== Auteurs URLs ==================
    path('auteurs/ajout/', views.ajout_auteur, name='ajout_auteur'),
    path('auteurs/', views.affiche_tout_auteur, name='affiche_tout_auteur'), # On peut voir tout les jeux de chaque auteurs en dessous de leurs informations
    path('auteurs/update/<int:id>/', views.update_auteur, name='update_auteur'),
    path('auteurs/delete/<int:id>/', views.delete_auteur, name='delete_auteur'),
    path('auteurs/confirmation_delete/<int:id>/', views.confirmation_delete_auteur, name='confirmation_delete_auteur'),

    # ================== Catégories URLs ==================
    path('categories/ajout/', views.ajout_categorie, name='ajout_categorie'),
    path('categories/', views.affiche_tout_categorie, name='affiche_tout_categorie'),
    path('categories/update/<int:id>/', views.update_categorie, name='update_categorie'),
    path('categories/delete/<int:id>/', views.delete_categorie, name='delete_categorie'),
    path('categories/confirmation_delete/<int:id>/', views.confirmation_delete_categorie, name='confirmation_delete_categorie'),

    # ================== Jeux URLs ==================
    path('jeux/ajout/', views.ajout_jeu, name='ajout_jeu'),
    path('jeux/', views.affiche_tout_jeu, name='affiche_tout_jeu'),
    path('jeux/<int:id>/', views.detail_jeu, name='detail_jeu'),   # Commentaires visible
    path('jeux/update/<int:id>/', views.update_jeu, name='update_jeu'),
    path('jeux/delete/<int:id>/', views.delete_jeu, name='delete_jeu'),
    path('jeux/confirmation_delete/<int:id>/', views.confirmation_delete_jeu, name='confirmation_delete_jeu'),

    # ================== Joueurs URLs ==================
    path('joueurs/ajout/', views.inscription, name='inscription'), #
    path('joueurs/mon-profil/', views.mon_profil, name='mon_profil'),  # Authenticated user profile
    path('joueurs/update/<int:id>/', views.update_joueur, name='update_joueur'),
    path('joueurs/traitement_update/<int:id>/', views.traitement_update_joueur, name='traitement_update_joueur'),
    path('joueurs/delete/<int:id>/', views.delete_joueur, name='delete_joueur'),
    path('joueurs/confirmation_delete/<int:id>/', views.confirmation_delete_joueur, name='confirmation_delete_joueur'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),

    # ================== Commentaires URLs ==================
    # Comment handling within game views
    path('jeux/<int:jeu_id>/commentaires/ajout/', views.ajout_commentaire, name='ajout_commentaire'),
    path('jeux/<int:jeu_id>/commentaires/update/<int:id>/', views.update_commentaire, name='update_commentaire'),
    path('jeux/<int:jeu_id>/commentaires/delete/<int:id>/', views.delete_commentaire, name='delete_commentaire'),

    # ================== Liste URLs ==================
    path('ma_jeux/<int:id>/', views.user_list, name='ma_liste'), # en fonction de l'ID de l'utilisateur donc il doit être authentificé
]