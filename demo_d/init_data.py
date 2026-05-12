"""
Rôle de ce fichier dans Django :
Ce script externe initialise des données de test pour l'application conges.
Il prépare Django avec django.setup(), puis crée des utilisateurs et profils utilisables en local.
"""

import os  # On utilise os pour définir la variable d'environnement des settings Django.

import django  # On importe Django pour initialiser son registre d'applications.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # On indique quel fichier settings Django doit charger.
django.setup()  # On initialise Django avant d'importer et manipuler les modèles.

from django.contrib.auth.models import User  # On importe User après django.setup() pour accéder correctement aux modèles.

from conges.models import Employe  # On importe le profil congés à créer pour les utilisateurs de test.


def create_user(username, password, is_staff=False, is_superuser=False):
    """Crée ou met à jour un utilisateur de test.

    Cette fonction centralise la création pour éviter de répéter le même code.
    Elle retourne l'utilisateur Django créé ou déjà existant.
    """

    user, created = User.objects.get_or_create(username=username)  # On récupère l'utilisateur s'il existe déjà.
    user.is_staff = is_staff  # Le statut staff donne accès à l'admin et au rôle responsable.
    user.is_superuser = is_superuser  # Le superuser possède tous les droits dans l'admin Django.
    user.set_password(password)  # set_password chiffre le mot de passe au lieu de le stocker en clair.
    user.save()  # On sauvegarde les changements en base SQLite.
    return user  # On renvoie l'utilisateur pour pouvoir créer son profil si besoin.


admin_user = create_user('admin', 'admin123', is_staff=True, is_superuser=True)  # Compte administrateur complet.
employe_user = create_user('employe1', 'employe123')  # Compte employé simple sans droits staff.
responsable_user = create_user('responsable1', 'responsable123', is_staff=True)  # Compte responsable basé sur is_staff.

Employe.objects.get_or_create(user=employe_user, defaults={'solde_conges': 25})  # Profil congés pour l'employé de test.
Employe.objects.get_or_create(user=responsable_user, defaults={'solde_conges': 25})  # Profil utile si le responsable soumet aussi un congé.

print('Données initiales créées ou mises à jour.')  # Message de fin lisible dans le terminal.
print('admin / admin123')  # Identifiants de l'administrateur.
print('employe1 / employe123')  # Identifiants de l'employé.
print('responsable1 / responsable123')  # Identifiants du responsable.
