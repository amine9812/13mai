"""
Rôle de ce fichier dans Django :
Ce fichier décrit la configuration de l'application conges.
Django l'utilise pour identifier et charger correctement cette application.
"""

from django.apps import AppConfig  # On importe la classe de configuration de base fournie par Django.


class CongesConfig(AppConfig):
    """Déclare la configuration principale de l'application conges.

    Cette classe donne à Django le nom Python de l'application.
    Elle retourne une configuration lue automatiquement au démarrage.
    """

    name = 'conges'
