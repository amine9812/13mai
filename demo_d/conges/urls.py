"""
Rôle de ce fichier dans Django :
Ce fichier contient les routes URL propres à l'application conges.
Chaque route relie une adresse du navigateur à une vue Python.
"""

from django.urls import path  # On importe path pour déclarer des routes simples.

from . import views  # On importe les vues de l'application conges.


app_name = 'conges'  # Ce namespace évite les conflits avec les noms d'URL d'autres applications.

urlpatterns = [  # Cette liste est lue par Django pour savoir quelles routes existent.
    path('', views.dashboard_view, name='dashboard'),  # La racine de l'app redirige selon le rôle.
    path('login/', views.login_view, name='login'),  # Cette route affiche et traite la connexion.
    path('logout/', views.logout_view, name='logout'),  # Cette route ferme la session utilisateur.
    path('employe/', views.employe_home, name='employe_home'),  # Cette route affiche l'espace employé.
    path('historique/', views.historique_demandes, name='historique_demandes'),  # Cette route affiche l'historique adapté au rôle.
    path('soumettre/', views.soumettre_demande, name='soumettre_demande'),  # Cette route affiche le formulaire de demande.
    path('responsable/', views.responsable_home, name='responsable_home'),  # Cette route affiche les demandes à traiter.
    path('traiter/<int:demande_id>/', views.traiter_demande, name='traiter_demande'),  # Cette route traite une demande précise.
]
