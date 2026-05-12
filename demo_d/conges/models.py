"""
Rôle de ce fichier dans Django :
Ce fichier contient les modèles de l'application conges.
Un modèle Django décrit une table de base de données et les champs stockés dans cette table.
"""

from django.contrib.auth.models import User  # On réutilise le modèle User intégré pour gérer les comptes et mots de passe.
from django.db import models  # On importe l'outil principal de Django pour déclarer des modèles de base de données.


class Employe(models.Model):
    """Représente le profil congés d'un utilisateur Django.

    Cette classe ajoute un solde de congés au compte User standard de Django.
    Elle retourne une représentation texte lisible avec le nom d'utilisateur.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Chaque employé est lié à un seul compte utilisateur Django.
    solde_conges = models.IntegerField(default=25)  # Le solde démarre à 25 jours pour simplifier la gestion locale.

    def __str__(self):
        """Retourne le nom de l'utilisateur associé à l'employé.

        Cette méthode aide Django Admin et les templates à afficher un libellé clair.
        Elle retourne une chaîne contenant le username.
        """

        return self.user.username  # On affiche le username car il identifie simplement l'employé.


class DemandeConge(models.Model):
    """Représente une demande de congé soumise par un employé.

    Cette classe stocke les dates, le type, le motif, le statut et la date de soumission.
    Elle retourne une représentation texte résumant la demande.
    """

    TYPE_CHOICES = [  # Les choix limitent les valeurs possibles pour éviter les textes libres incohérents.
        ('annuel', 'Congé annuel'),  # Valeur stockée en base puis libellé affiché dans les formulaires.
        ('maladie', 'Congé maladie'),  # Valeur utilisée pour un arrêt ou une absence maladie.
        ('autre', 'Autre'),  # Valeur générique pour les autres motifs de congé.
    ]

    STATUT_CHOICES = [  # Les choix de statut encadrent le cycle de traitement d'une demande.
        ('en_attente', 'En attente'),  # Statut initial juste après la soumission.
        ('validee', 'Validée'),  # Statut utilisé quand le responsable accepte la demande.
        ('refusee', 'Refusée'),  # Statut utilisé quand le responsable rejette la demande.
    ]

    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)  # Une demande appartient à un employé.
    date_debut = models.DateField()  # DateField stocke une date sans heure pour le début du congé.
    date_fin = models.DateField()  # DateField stocke une date sans heure pour la fin du congé.
    type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)  # CharField stocke un court texte limité aux choix définis.
    motif = models.TextField(blank=True)  # TextField accepte un texte long et blank=True rend le motif optionnel.
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')  # Le statut commence toujours en attente.
    date_soumission = models.DateTimeField(auto_now_add=True)  # Django renseigne automatiquement la date lors de la création.

    def __str__(self):
        """Retourne un résumé humain de la demande.

        Cette méthode rend les listes Django Admin plus faciles à lire.
        Elle retourne une chaîne avec l'employé et la période demandée.
        """

        return f'{self.employe} : {self.date_debut} au {self.date_fin}'  # On résume la demande par son auteur et ses dates.
