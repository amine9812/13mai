"""
Rôle de ce fichier dans Django :
Ce fichier déclare les modèles visibles dans l'interface d'administration Django.
L'administrateur peut ainsi gérer les employés et les demandes depuis /admin/.
"""

from django.contrib import admin  # On importe le site d'administration fourni par Django.

from .models import DemandeConge, Employe  # On importe les modèles que l'on veut rendre administrables.


@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    """Configure l'affichage des employés dans l'administration.

    Cette classe rend la liste plus lisible en montrant l'utilisateur et le solde.
    Elle retourne une configuration utilisée automatiquement par Django Admin.
    """

    list_display = ('user', 'solde_conges')  # Ces colonnes apparaissent dans la liste des employés.
    search_fields = ('user__username',)  # La recherche admin peut retrouver un employé par username.


@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
    """Configure l'affichage des demandes de congé dans l'administration.

    Cette classe aide l'administrateur à filtrer et lire rapidement les demandes.
    Elle retourne une configuration utilisée automatiquement par Django Admin.
    """

    list_display = ('employe', 'date_debut', 'date_fin', 'type_conge', 'statut', 'date_soumission')  # Ces colonnes résument chaque demande.
    list_filter = ('statut', 'type_conge')  # Ces filtres permettent de trier les demandes par statut ou type.
    search_fields = ('employe__user__username', 'motif')  # La recherche porte sur l'employé et le motif.
