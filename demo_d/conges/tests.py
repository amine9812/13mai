"""
Rôle de ce fichier dans Django :
Ce fichier vérifie les comportements importants de l'application conges.
Les tests couvrent notamment l'historique des demandes selon le rôle utilisateur.
"""

from django.contrib.auth.models import User  # On crée des utilisateurs Django pour tester les droits.
from django.test import TestCase  # TestCase fournit une base isolée et un client HTTP de test.
from django.urls import reverse  # reverse évite d'écrire les URL en dur dans les tests.

from .models import DemandeConge, Employe  # Les tests créent des profils et des demandes de congé.


class HistoriqueDemandesTests(TestCase):
    """Vérifie que l'historique respecte le rôle de l'utilisateur connecté."""

    def setUp(self):
        """Prépare deux employés, un responsable et un administrateur."""

        self.employe_user = User.objects.create_user(username='employe1', password='employe123')
        self.autre_user = User.objects.create_user(username='employe2', password='employe234')
        self.responsable_user = User.objects.create_user(
            username='responsable1',
            password='responsable123',
            is_staff=True,
        )
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        self.employe = Employe.objects.create(user=self.employe_user)
        self.autre_employe = Employe.objects.create(user=self.autre_user)

        DemandeConge.objects.create(
            employe=self.employe,
            date_debut='2026-06-01',
            date_fin='2026-06-03',
            type_conge='annuel',
            motif='Vacances employe visible',
            statut='validee',
        )
        DemandeConge.objects.create(
            employe=self.autre_employe,
            date_debut='2026-07-01',
            date_fin='2026-07-02',
            type_conge='maladie',
            motif='Demande autre employe privee',
            statut='refusee',
        )

    def test_employe_ne_voit_que_son_historique(self):
        """Un employé simple ne voit pas les demandes des autres utilisateurs."""

        self.client.login(username='employe1', password='employe123')
        response = self.client.get(reverse('conges:historique_demandes'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mon historique')
        self.assertContains(response, 'Vacances employe visible')
        self.assertNotContains(response, 'Demande autre employe privee')
        self.assertNotContains(response, 'employe2')

    def test_responsable_voit_tout_l_historique(self):
        """Un responsable staff voit toutes les demandes."""

        self.client.login(username='responsable1', password='responsable123')
        response = self.client.get(reverse('conges:historique_demandes'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Historique des demandes')
        self.assertContains(response, 'Vacances employe visible')
        self.assertContains(response, 'Demande autre employe privee')
        self.assertContains(response, 'employe1')
        self.assertContains(response, 'employe2')

    def test_admin_voit_tout_l_historique(self):
        """Un administrateur superuser voit aussi toutes les demandes."""

        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('conges:historique_demandes'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vacances employe visible')
        self.assertContains(response, 'Demande autre employe privee')
