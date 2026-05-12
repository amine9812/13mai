"""
Rôle de ce fichier dans Django :
Ce fichier contient les formulaires de l'application conges.
Un formulaire Django valide les données reçues depuis une page HTML avant de les enregistrer.
"""

from django import forms  # On importe le module forms pour construire des formulaires Django.

from .models import DemandeConge  # On importe le modèle utilisé comme base du formulaire.


class DemandeCongeForm(forms.ModelForm):
    """Construit le formulaire de soumission d'une demande de congé.

    Cette classe expose uniquement les champs que l'employé peut choisir.
    Elle retourne un formulaire capable de valider puis créer une DemandeConge.
    """

    class Meta:
        """Déclare le modèle et les champs utilisés par le formulaire.

        Cette classe interne indique à Django comment générer les champs HTML.
        Elle retourne une configuration lue par ModelForm.
        """

        model = DemandeConge  # Le formulaire s'appuie sur le modèle DemandeConge.
        fields = ['date_debut', 'date_fin', 'type_conge', 'motif']  # Le statut est exclu car seul le responsable le décide.
        widgets = {  # Les widgets personnalisent le rendu HTML des champs.
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Le navigateur affiche un sélecteur de date.
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Le navigateur affiche un sélecteur de date.
            'type_conge': forms.Select(attrs={'class': 'form-select'}),  # Bootstrap stylise la liste déroulante.
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  # Bootstrap stylise la zone de texte.
        }
