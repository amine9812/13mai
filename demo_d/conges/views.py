"""
Rôle de ce fichier dans Django :
Ce fichier contient les vues de l'application conges.
Une vue reçoit une requête HTTP, applique la logique métier, puis renvoie une réponse HTML ou une redirection.
"""

from django.contrib import messages  # On utilise les messages pour afficher des retours simples à l'utilisateur.
from django.contrib.auth import authenticate, login, logout  # Ces fonctions gèrent la connexion et la déconnexion Django.
from django.contrib.auth.decorators import login_required  # Ce décorateur bloque l'accès aux pages privées.
from django.contrib.auth.forms import AuthenticationForm  # Ce formulaire standard vérifie username et password.
from django.shortcuts import get_object_or_404, redirect, render  # Ces raccourcis simplifient les réponses Django.

from .forms import DemandeCongeForm  # On importe le formulaire de création de demande.
from .models import DemandeConge, Employe  # On importe les modèles nécessaires aux pages.


def login_view(request):
    """Affiche et traite le formulaire de connexion.

    Cette vue utilise authenticate pour vérifier les identifiants, puis login pour ouvrir la session.
    Elle retourne la page de connexion ou redirige vers le tableau de bord si la connexion réussit.
    """

    form = AuthenticationForm(request, data=request.POST or None)  # Le formulaire reçoit les données POST seulement quand elles existent.
    form.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    form.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})
    if request.method == 'POST':  # Une requête POST signifie que l'utilisateur vient d'envoyer le formulaire.
        username = request.POST.get('username')  # On lit le nom d'utilisateur envoyé par le navigateur.
        password = request.POST.get('password')  # On lit le mot de passe envoyé par le navigateur.
        user = authenticate(request, username=username, password=password)  # Django vérifie les identifiants contre la base.
        if user is not None:  # Si un utilisateur est trouvé, les identifiants sont corrects.
            login(request, user)  # Django enregistre l'utilisateur dans la session.
            return redirect('conges:dashboard')  # Après connexion, on envoie l'utilisateur vers l'accueil intelligent.
        messages.error(request, 'Identifiants incorrects.')  # On affiche une erreur si la connexion échoue.

    return render(request, 'conges/login.html', {'form': form})  # render combine le template avec les données du contexte.


@login_required
def logout_view(request):
    """Déconnecte l'utilisateur courant.

    Cette vue ferme la session Django pour protéger l'accès aux pages privées.
    Elle retourne une redirection vers la page de connexion.
    """

    logout(request)  # Django supprime l'utilisateur connecté de la session.
    return redirect('conges:login')  # On revient à la page de connexion après la déconnexion.


@login_required
def dashboard_view(request):
    """Redirige l'utilisateur vers la page adaptée à son rôle.

    Cette vue utilise is_staff pour orienter les responsables et administrateurs vers l'écran de validation.
    Elle retourne une redirection vers l'espace employé ou responsable.
    """

    if request.user.is_staff:  # Dans cette application simple, un staff Django joue le rôle responsable ou administrateur.
        return redirect('conges:responsable_home')  # Les responsables voient les demandes à traiter.
    return redirect('conges:employe_home')  # Les employés voient leur solde et leur historique.


@login_required
def employe_home(request):
    """Affiche le solde et l'historique de l'employé connecté.

    Cette vue récupère ou crée le profil Employe associé au User Django.
    Elle retourne une page HTML avec le solde et les demandes de l'employé.
    """

    employe, created = Employe.objects.get_or_create(user=request.user)  # On garantit qu'un profil existe pour l'utilisateur connecté.
    demandes = DemandeConge.objects.filter(employe=employe).order_by('-date_soumission')  # On liste les demandes les plus récentes d'abord.
    context = {
        'employe': employe,
        'demandes': demandes,
        'created': created,
        'demandes_total': demandes.count(),
        'demandes_en_attente': demandes.filter(statut='en_attente').count(),
        'demandes_validees': demandes.filter(statut='validee').count(),
    }  # Le contexte contient les données transmises au template.
    return render(request, 'conges/employe_home.html', context)  # Le template reçoit le solde et l'historique.


@login_required
def historique_demandes(request):
    """Affiche l'historique des demandes selon le rôle de l'utilisateur.

    Les responsables et administrateurs voient toutes les demandes.
    Un employé simple voit uniquement ses propres demandes.
    """

    can_view_all = request.user.is_staff or request.user.is_superuser  # Les rôles avec droits voient l'historique global.
    demandes = DemandeConge.objects.select_related('employe__user').order_by('-date_soumission')  # Base commune triée par récent.
    if not can_view_all:  # Un employé simple ne doit pas lire les demandes des autres.
        employe, created = Employe.objects.get_or_create(user=request.user)  # On garantit son profil avant de filtrer.
        demandes = demandes.filter(employe=employe)  # L'historique reste personnel pour l'employé.

    context = {
        'can_view_all': can_view_all,
        'demandes': demandes,
    }  # Le template adapte le titre et les colonnes selon ce droit.
    return render(request, 'conges/historique_demandes.html', context)  # Page d'historique commune à tous les rôles.


@login_required
def soumettre_demande(request):
    """Affiche et traite le formulaire de soumission de congé.

    Cette vue crée une demande liée à l'employé connecté avec le statut par défaut en attente.
    Elle retourne le formulaire ou redirige vers l'espace employé après enregistrement.
    """

    employe, created = Employe.objects.get_or_create(user=request.user)  # On crée le profil si l'utilisateur n'en a pas encore.
    form = DemandeCongeForm(request.POST or None)  # Le formulaire est vide en GET et rempli en POST.
    if request.method == 'POST' and form.is_valid():  # On enregistre seulement si la méthode et les données sont correctes.
        demande = form.save(commit=False)  # commit=False permet d'ajouter l'employé avant l'écriture en base.
        demande.employe = employe  # La demande appartient toujours à l'utilisateur connecté.
        demande.save()  # On écrit la demande en base avec le statut par défaut.
        messages.success(request, 'Votre demande a été soumise.')  # On confirme la création à l'utilisateur.
        return redirect('conges:employe_home')  # On retourne à l'historique après la soumission.

    return render(request, 'conges/soumettre_demande.html', {'form': form})  # On affiche le formulaire au navigateur.


@login_required
def responsable_home(request):
    """Affiche les demandes en attente pour le responsable.

    Cette vue limite l'accès aux utilisateurs staff afin de représenter le rôle Responsable.
    Elle retourne une page contenant toutes les demandes encore non traitées.
    """

    if not request.user.is_staff:  # Un employé simple ne doit pas accéder à la validation.
        return redirect('conges:employe_home')  # On le renvoie vers son propre espace.
    demandes = DemandeConge.objects.filter(statut='en_attente').order_by('date_soumission')  # Les plus anciennes demandes sont traitées d'abord.
    context = {
        'demandes': demandes,
        'demandes_en_attente': demandes.count(),
        'demandes_total': DemandeConge.objects.count(),
        'demandes_validees': DemandeConge.objects.filter(statut='validee').count(),
        'demandes_refusees': DemandeConge.objects.filter(statut='refusee').count(),
    }  # Les compteurs alimentent le tableau de bord responsable.
    return render(request, 'conges/responsable_home.html', context)  # Le template affiche le tableau de validation.


@login_required
def traiter_demande(request, demande_id):
    """Valide ou refuse une demande selon le bouton cliqué.

    Cette vue lit l'action envoyée en POST par le responsable et met à jour le statut.
    Elle retourne une redirection vers la liste des demandes en attente.
    """

    if not request.user.is_staff:  # Seuls les responsables et administrateurs peuvent traiter les demandes.
        return redirect('conges:employe_home')  # Un employé est redirigé vers son espace personnel.
    demande = get_object_or_404(DemandeConge, id=demande_id)  # On récupère la demande ou on renvoie une erreur 404.
    if request.method == 'POST':  # Le changement de statut doit venir d'un formulaire POST.
        action = request.POST.get('action')  # Le bouton cliqué envoie l'action souhaitée.
        if action == 'valider':  # Le responsable a choisi d'accepter la demande.
            demande.statut = 'validee'  # On met à jour le statut avec la valeur prévue par le modèle.
            messages.success(request, 'La demande a été validée.')  # On confirme l'action dans l'interface.
        elif action == 'refuser':  # Le responsable a choisi de refuser la demande.
            demande.statut = 'refusee'  # On met à jour le statut avec la valeur prévue par le modèle.
            messages.warning(request, 'La demande a été refusée.')  # On confirme le refus dans l'interface.
        demande.save()  # On sauvegarde la modification en base.

    return redirect('conges:responsable_home')  # Après traitement, on revient à la file d'attente.
