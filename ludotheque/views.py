from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Avg, Count
from .models import Auteurs, Categories, Commentaires, Jeux, Joueurs, ListeJeux
from .forms import AuteurForm, CategorieForm, JeuForm, JoueurForm, CommentaireForm, ListeJeuxForm
from django.contrib import messages
from .wrappers import login_required
from django.contrib.auth.hashers import check_password


def index(request):
    """Vue pour la page d'accueil"""
    # Récupération des données pour la page d'accueil
    jeux_populaires = Jeux.objects.annotate(
        note_moyenne=Avg('commentaires__note'),
        nb_avis=Count('commentaires')
    ).order_by('-note_moyenne')[:6]

    derniers_jeux = Jeux.objects.order_by('-id')[:6]

    auteurs_populaires = Auteurs.objects.annotate(note_moyenne=Avg('jeux__commentaires__note')).order_by('-note_moyenne')[:4]

    context = {
        'jeux_populaires': jeux_populaires,
        'derniers_jeux': derniers_jeux,
        'auteurs_populaires': auteurs_populaires,
    }
    return render(request, 'ludotheque/index.html', context)



def affiche_tout_auteur(request):
    auteurs = Auteurs.objects.all()
    return render(request, 'ludotheque/auteurs/liste.html', {'auteurs': auteurs})

def ajout_auteur(request):
    if request.method == 'POST':
        form = AuteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('affiche_tout_auteur')
    else:
        form = AuteurForm()
    return render(request, 'ludotheque/auteurs/form.html', {'form': form})

def update_auteur(request, id):
    auteur = get_object_or_404(Auteurs, pk=id)
    if request.method == 'POST':
        form = AuteurForm(request.POST, instance=auteur)
        if form.is_valid():
            form.save()
            return redirect('affiche_tout_auteur')
    else:
        form = AuteurForm(instance=auteur)
    return render(request, 'ludotheque/auteurs/form.html', {'form': form})

def confirmation_delete_auteur(request, id):
    auteur = get_object_or_404(Auteurs, pk=id)
    return render(request, 'ludotheque/auteurs/confirmation_delete.html', {'auteur': auteur})

def delete_auteur(request, id):
    auteur = get_object_or_404(Auteurs, pk=id)
    auteur.delete()
    return redirect('affiche_tout_auteur')


def detail_jeu(request, id):
    jeu = get_object_or_404(Jeux, pk=id)

    # Moyennes par type de joueur
    moyennes = Commentaires.objects.filter(jeu=jeu).values('joueur__type').annotate(
        moyenne=Avg('note')
    )

    # Meilleur et pire commentaire
    meilleur_commentaire = Commentaires.objects.filter(jeu=jeu).order_by('-note').first()
    pire_commentaire = Commentaires.objects.filter(jeu=jeu).order_by('note').first()

    return render(request, 'ludotheque/jeux/detail.html', {
        'jeu': jeu,
        'moyennes': moyennes,
        'meilleur_commentaire': meilleur_commentaire,
        'pire_commentaire': pire_commentaire
    })


# Vue d'inscription
def inscription(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connecter l'utilisateur manuellement
            request.session['joueur_id'] = user.id
            messages.success(request, f'Bienvenue {user.email}, votre compte a été créé avec succès!')
            return redirect('ludotheque:index')
    else:
        form = JoueurForm()
    return render(request, 'ludotheque/inscription.html', {'form': form})


# Vue de connexion
def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Joueurs.objects.get(email=email)
        except Joueurs.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.mot_de_passe):
            request.session['joueur_id'] = user.id
            return redirect('ludotheque:index')
        else:
            messages.error(request, 'Identifiants invalides')

    return render(request, 'ludotheque/connexion.html')


# Vue de déconnexion
def deconnexion(request):
    if 'joueur_id' in request.session:
        del request.session['joueur_id']
    return redirect('ludotheque:index')


# Vue du profil
@login_required
def mon_profil(request):
    joueur_id = request.session.get('joueur_id')
    if not joueur_id:
        return redirect('ludotheque:connexion')

    try:
        joueur = Joueurs.objects.get(id=joueur_id)
    except Joueurs.DoesNotExist:
        return redirect('ludotheque:connexion')

    return render(request, 'ludotheque/account.html', {'joueur': joueur})

# ================== Categorie Views ==================
def ajout_categorie(request):
    if request.method == 'POST':
        # Process form data
        return redirect('affiche_tout_categorie')
    return render(request, 'ajout_categorie.html')

def affiche_tout_categorie(request):
    categories = Categories.objects.all()
    return render(request, 'affiche_tout_categorie.html', {'categories': categories})

def update_categorie(request, id):
    categorie = get_object_or_404(Categories, pk=id)
    if request.method == 'POST':
        # Update logic
        return redirect('affiche_tout_categorie')
    return render(request, 'update_categorie.html', {'categorie': categorie})

def confirmation_delete_categorie(request, id):
    categorie = get_object_or_404(Categories, pk=id)
    return render(request, 'confirmation_delete_categorie.html', {'categorie': categorie})

def delete_categorie(request, id):
    categorie = get_object_or_404(Categories, pk=id)
    categorie.delete()
    return redirect('affiche_tout_categorie')

# ================== Jeu Views ==================

def ajout_jeu(request):
    if request.method == 'POST':
        form = JeuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('affiche_tout_jeu')
    else:
        form = JeuForm()

    return render(request, 'ludotheque/jeux/ajout_jeux.html', {'form': form,})

def affiche_tout_jeu(request):
    jeux = Jeux.objects.annotate(
        note_moyenne=Avg('commentaires__note'),
        nb_commentaires=Count('commentaires')
    ).all()

    return render(request, 'ludotheque/jeux/liste.html', {
        'jeux': jeux,
        'title': 'Tous les jeux'
    })

def detail_jeu(request, id):
    jeu = get_object_or_404(Jeux, pk=id)

    # Calcul des moyennes par type de joueur
    moyennes = Commentaires.objects.filter(jeu=jeu).values('joueur__type').annotate(
        moyenne=Avg('note')
    )

    # Meilleur et pire commentaire
    meilleur_commentaire = Commentaires.objects.filter(jeu=jeu).order_by('-note').first()
    pire_commentaire = Commentaires.objects.filter(jeu=jeu).order_by('note').first()

    # Commentaires pour ce jeu
    commentaires = Commentaires.objects.filter(jeu=jeu).select_related('joueur')

    return render(request, 'ludotheque/jeux/detail.html', {
        'jeu': jeu,
        'moyennes': moyennes,
        'meilleur_commentaire': meilleur_commentaire,
        'pire_commentaire': pire_commentaire,
        'commentaires': commentaires
    })

def update_jeu(request, id):
    jeu = get_object_or_404(Jeux, pk=id)

    if request.method == 'POST':
        form = JeuForm(request.POST, request.FILES, instance=jeu)
        if form.is_valid():
            form.save()
            return redirect('detail_jeu', id=id)
    else:
        form = JeuForm(instance=jeu)

    return render(request, 'ludotheque/jeux/ajout.html', {
        'form': form,
        'title': f'Modifier {jeu.titre}',
        'update': True
    })

def confirmation_delete_jeu(request, id):
    jeu = get_object_or_404(Jeux, pk=id)
    return render(request, 'ludotheque/jeux/confirmation_delete.html', {
        'jeu': jeu,
        'title': f'Supprimer {jeu.titre}?'
    })

def delete_jeu(request, id):
    jeu = get_object_or_404(Jeux, pk=id)
    jeu.delete()
    return redirect('affiche_tout_jeu')

# ================== Joueur Views ==================
def ajout_joueur(request):
    if request.method == 'POST':
        form = JoueurForm(request)
        if form.is_valid():
            joueur = form.save()
            return render(request, "ludotheque/affiche_joueur.html", {"joueur": joueur})
        else:
            return render(request, 'ludotheque/inscription.html', {'form': form})
    else:
        form = JoueurForm()
        return render(request, 'ludotheque/inscription.html', {'form': form})

@login_required
def mon_profil(request):
    joueur = request.user
    return render(request, 'ludotheque/account.html', {'joueur': joueur})

def update_joueur(request, id):
    joueur = Joueurs.objects.get(pk=id)
    Jform = JoueurForm(joueur.__dict__)
    return render(request, "ludotheque/update_joueur.html", {"form": Jform, "id": id})

def traitement_update_joueur(request, id):
    Jform = JoueurForm(request.POST)
    if Jform.is_valid():
        joueur = Jform.save(commit=False)
        joueur.id = id
        joueur.save()
        return HttpResponseRedirect("/ludotheque/joueurs/mon-profil/")
    else:
        return render(request, "ludotheque/update_joueur.html", {"form": Jform, "id": id})

def confirmation_delete_joueur(request, id):
    joueur = get_object_or_404(Joueurs, pk=id)
    return render(request, 'confirmation_delete_joueur.html', {'joueur': joueur})

def delete_joueur(request, id):
    joueur = get_object_or_404(Joueurs, pk=id)
    joueur.delete()
    return redirect('index')

# ================== Commentaire Views ==================
def ajout_commentaire(request, jeu_id):
    jeu = get_object_or_404(Jeux, pk=jeu_id)
    if request.method == 'POST':
        # Add comment logic
        return redirect('detail_jeu', id=jeu_id)
    return render(request, 'ajout_commentaire.html', {'jeu': jeu})

def update_commentaire(request, jeu_id, id):
    commentaire = get_object_or_404(Commentaires, pk=id)
    if request.method == 'POST':
        # Update comment
        return redirect('detail_jeu', id=jeu_id)
    return render(request, 'update_commentaire.html', {'commentaire': commentaire})

def delete_commentaire(request, jeu_id, id):
    commentaire = get_object_or_404(Commentaires, pk=id)
    commentaire.delete()
    return redirect('detail_jeu', id=jeu_id)

# ================== Liste Views ==================
def user_list(request, id):
    joueur = get_object_or_404(Joueurs, pk=id)
    jeux = joueur.liste_de_souhaits.all()  # Assuming many-to-many relationship
    return render(request, 'ma_liste.html', {'joueur': joueur, 'jeux': jeux})