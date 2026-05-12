# Guide complet du projet – Application de gestion des demandes de congés

## Introduction : C'est quoi ce projet ?

Cette application est un petit site web local pour gérer des demandes de congés. Un **employé** peut se connecter, voir son solde de congés, consulter l'historique de ses demandes et envoyer une nouvelle demande avec une date de début, une date de fin, un type et un motif. Un **responsable** peut se connecter, voir toutes les demandes en attente, puis les valider ou les refuser. Un **administrateur** utilise l'admin Django par défaut pour gérer les comptes et vérifier les données.

Imaginons Paul, employé. Paul ouvre le site, tape son nom d'utilisateur et son mot de passe, puis arrive sur son espace personnel. Il voit qu'il a 25 jours de congés, clique sur "Nouvelle demande", choisit ses dates, écrit un motif et envoie. Sa demande apparaît avec le statut "En attente". Marie, sa responsable, se connecte ensuite avec son compte responsable, voit la demande de Paul dans un tableau et clique sur "Valider". Quand Paul revient sur son espace, il voit que sa demande est maintenant "Validée". Dans le code actuel, le statut change bien ; le solde est affiché mais n'est pas automatiquement diminué.

Django est le framework web utilisé ici. Un **framework** est une boîte à outils qui donne déjà les grandes pièces nécessaires pour construire un site. 🧩 Analogie : Django ressemble à une cuisine de restaurant. Le serveur prend la commande du client, la cuisine prépare le plat, puis le serveur apporte l'assiette. Dans Django, l'URL reçoit l'adresse demandée, la vue prépare la réponse, le modèle parle à la base de données, et le template affiche joliment la page.

---

## Partie 1 – Les fichiers que tu n'as pas codés (mais qu'il faut comprendre)

### 📁 manage.py

Ce fichier a été créé automatiquement par Django, tu n'as pas à le modifier pour ce projet.

`manage.py` est la télécommande du projet. Il permet de lancer des commandes Django depuis le terminal. Dans ce projet, il indique d'abord à Django où se trouve la configuration :

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```

Cela veut dire : "Django, utilise le fichier `config/settings.py` comme mode d'emploi principal."

🧩 Analogie : `manage.py`, c'est la télécommande d'une télévision. Tu n'ouvres pas la télé pour changer de chaîne ; tu appuies sur des boutons. Ici, tu n'ouvres pas Django à la main ; tu tapes des commandes.

Commandes importantes :

- `python manage.py runserver` : lance le site en local, comme ouvrir la boutique pour tester.
- `python manage.py makemigrations` : demande à Django de préparer les plans de modification de la base de données.
- `python manage.py migrate` : applique ces plans dans la base de données.
- `python manage.py createsuperuser` : crée un compte administrateur très puissant pour accéder à `/admin/`.

Si `manage.py` n'existait pas, tu pourrais encore utiliser Django autrement, mais ce serait beaucoup moins simple. Pour un débutant, ce serait comme perdre la télécommande et devoir appuyer sur de minuscules boutons derrière l'appareil.

### 📁 db.sqlite3

Ce fichier a été créé automatiquement par Django, tu n'as pas à le modifier pour ce projet.

`db.sqlite3` est la base de données locale. Une **base de données** est l'endroit où l'application range les informations : utilisateurs, employés, demandes de congés, statuts, dates, etc.

🧩 Analogie : imagine un grand classeur Excel avec plusieurs feuilles. Une feuille contient les utilisateurs, une autre les employés, une autre les demandes. SQLite est une base de données simple qui tient dans un seul fichier, donc elle est parfaite pour apprendre, tester et travailler localement.

Si `db.sqlite3` n'existait pas, le site pourrait démarrer, mais il n'aurait aucune table pour stocker les données. Après `migrate`, Django peut le recréer.

### 📁 Les fichiers __init__.py

Ce fichier a été créé automatiquement par Django, tu n'as pas à le modifier pour ce projet.

Les fichiers `__init__.py` disent à Python : "ce dossier est un module importable". Un **module** est un morceau de code que Python peut retrouver et utiliser.

Dans ce projet, on en trouve par exemple dans :

- `config/__init__.py`
- `conges/__init__.py`
- `conges/migrations/__init__.py`

🧩 Analogie : c'est comme une étiquette sur une boîte de rangement. Sans étiquette, tu vois une boîte, mais tu ne sais pas forcément qu'elle fait partie du système organisé.

Si ces fichiers n'existaient pas, certains imports Python pourraient ne pas fonctionner selon la version et l'organisation du projet. Django aurait plus de mal à reconnaître correctement les dossiers comme des parties du projet.

### 📁 Les fichiers migrations/

Ce fichier a été créé automatiquement par Django, tu n'as pas à le modifier pour ce projet.

Le dossier `conges/migrations/` contient les instructions que Django suit pour construire ou modifier les tables dans `db.sqlite3`. Dans ce projet, `0001_initial.py` explique comment créer les tables `Employe` et `DemandeConge`.

🧩 Analogie : les migrations sont des plans de construction. Si le modèle `Employe` est une idée de pièce à construire, la migration est le plan donné aux ouvriers : "ajoute un mur ici, une porte là, une fenêtre là".

On ne modifie pas les migrations à la main dans un projet normal, car elles représentent l'historique des transformations de la base. Si tu changes ces plans n'importe comment, Django peut ne plus savoir dans quel état se trouve la base.

Si les migrations n'existaient pas, Django verrait les modèles Python mais ne saurait pas comment créer les tables correspondantes dans SQLite.

---

## Partie 2 – Les fichiers que tu as codés (le cœur du projet)

### Nom du fichier : config/settings.py

**Rôle dans l'application :**
Ce fichier contient les grands réglages du projet Django, et la partie importante ici est l'enregistrement de l'application `conges`.

**Analogie :**
🧩 `settings.py`, c'est le tableau électrique d'une maison : il indique quelles pièces existent, quelle source d'énergie utiliser, et comment les circuits sont branchés.

**Explications ligne par ligne (ou bloc par bloc) :**

```python
SECRET_KEY = 'django-insecure-hhx!7a++5$x(4egzwrr4b*@d*srfv0m7p6=%txlpjk$uf%7t0u'
```

`SECRET_KEY` est une clé secrète utilisée par Django pour sécuriser certaines données, comme les sessions et les protections internes. C'est comme le tampon officiel d'une mairie : il prouve que certains papiers viennent bien du bon endroit.

```python
DEBUG = True
```

`DEBUG=True` veut dire que Django affiche des erreurs détaillées pendant le développement. C'est pratique pour apprendre, mais à ne pas utiliser tel quel sur un vrai site public.

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']
```

`ALLOWED_HOSTS` liste les adresses autorisées à ouvrir le site. `localhost` et `127.0.0.1` désignent ton ordinateur. `testserver` sert aux tests internes de Django.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'conges',
]
```

`INSTALLED_APPS` est la liste des applications activées. Une **application Django** est un bloc du site avec ses modèles, vues, formulaires et templates. Les lignes `django.contrib...` sont des outils fournis par Django : admin, comptes utilisateurs, sessions, messages, fichiers statiques. La ligne importante ajoutée est :

```python
'conges',
```

Elle dit à Django : "charge aussi notre application de gestion de congés". Sans cette ligne, Django ignorerait les modèles `Employe` et `DemandeConge`.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

`DATABASES` explique où stocker les données. Ici, Django utilise SQLite, une base simple dans le fichier `db.sqlite3`.

```python
LOGIN_URL = 'conges:login'
```

`LOGIN_URL` indique à Django où envoyer un utilisateur non connecté quand il essaie d'ouvrir une page protégée.

**Scénario concret :**
Quand Paul ouvre `/employe/` sans être connecté, Django regarde `LOGIN_URL` et sait qu'il doit l'envoyer vers la page de connexion `conges:login`. Quand Django démarre, il lit aussi `INSTALLED_APPS` et charge l'application `conges`.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Le projet ne saurait pas quelles applications charger, quelle base utiliser, ni où rediriger les utilisateurs non connectés. Le site pourrait refuser de démarrer.

### Nom du fichier : conges/models.py

**Rôle dans l'application :**
Ce fichier décrit les objets importants stockés en base de données : les employés et les demandes de congé.

**Analogie :**
🧩 Un modèle Django, c'est comme un formulaire papier officiel que l'on range ensuite dans un classeur. Le modèle dit quelles cases existent : nom, date, type, statut. La base de données est le classeur où chaque formulaire rempli devient une ligne.

**Explications ligne par ligne (ou bloc par bloc) :**

```python
"""
Rôle de ce fichier dans Django :
Ce fichier contient les modèles de l'application conges.
Un modèle Django décrit une table de base de données et les champs stockés dans cette table.
"""
```

Ce commentaire explique le rôle du fichier. Une **table** est comme une feuille Excel : chaque colonne est un champ, chaque ligne est un objet enregistré.

```python
from django.contrib.auth.models import User
from django.db import models
```

`User` est le modèle utilisateur intégré de Django. Il contient déjà un nom d'utilisateur, un mot de passe, des droits, etc. `models` est la boîte à outils pour créer des modèles.

```python
class Employe(models.Model):
```

`Employe` est un modèle Django. `models.Model` veut dire : "cette classe doit devenir une table dans la base".

```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
```

`OneToOneField` crée un lien "un pour un" entre `Employe` et `User`. Chaque profil employé correspond à un seul compte Django. `on_delete=models.CASCADE` veut dire : si le compte User est supprimé, le profil Employe lié est supprimé aussi.

🧩 Analogie : c'est comme une carte de bibliothèque liée à une seule personne. Si la personne est retirée du registre, sa carte n'a plus de raison d'exister.

```python
solde_conges = models.IntegerField(default=25)
```

`IntegerField` stocke un nombre entier. Ici, le solde commence à 25 jours par défaut.

```python
def __str__(self):
    return self.user.username
```

`__str__` dit à Django comment afficher un employé sous forme de texte. Dans l'admin, au lieu de voir "Employe object (1)", on voit le username, par exemple `employe1`.

```python
class DemandeConge(models.Model):
```

`DemandeConge` est le modèle qui représente une demande de congé. Chaque objet correspond à une ligne dans la table des demandes.

```python
TYPE_CHOICES = [
    ('annuel', 'Congé annuel'),
    ('maladie', 'Congé maladie'),
    ('autre', 'Autre'),
]
```

`choices` est une liste de choix autorisés. La première valeur est stockée dans la base, la deuxième est affichée à l'utilisateur.

🧩 Analogie : c'est une liste déroulante sur un formulaire papier. Au lieu d'écrire n'importe quoi, on coche "Congé annuel", "Congé maladie" ou "Autre".

```python
STATUT_CHOICES = [
    ('en_attente', 'En attente'),
    ('validee', 'Validée'),
    ('refusee', 'Refusée'),
]
```

Cette liste limite les statuts possibles. Une demande ne peut être que "En attente", "Validée" ou "Refusée".

```python
employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
```

`ForeignKey` crée un lien entre deux tables. Ici, chaque demande connaît l'employé qui l'a faite.

🧩 Analogie : chaque facture connaît son client. La facture ne recopie pas toute la fiche client, elle garde un lien vers elle.

```python
date_debut = models.DateField()
date_fin = models.DateField()
```

`DateField` stocke une date sans heure. Ici, ce sont les deux bornes de la période demandée.

```python
type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)
```

`CharField` stocke un texte court. `max_length=20` limite la taille du texte. `choices=TYPE_CHOICES` force l'utilisateur à choisir parmi les types définis.

```python
motif = models.TextField(blank=True)
```

`TextField` stocke un texte plus long. `blank=True` signifie que le champ peut rester vide dans le formulaire.

```python
statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
```

Le statut est un texte court limité aux choix. `default='en_attente'` signifie qu'une nouvelle demande commence toujours en attente.

```python
date_soumission = models.DateTimeField(auto_now_add=True)
```

`DateTimeField` stocke une date avec l'heure. `auto_now_add=True` demande à Django de remplir automatiquement ce champ au moment de la création.

```python
def __str__(self):
    return f'{self.employe} : {self.date_debut} au {self.date_fin}'
```

Cette méthode affiche une demande sous une forme lisible, par exemple `employe1 : 2026-05-01 au 2026-05-05`.

**Scénario concret :**
Quand Paul soumet une demande, Django crée une nouvelle ligne `DemandeConge`. Cette ligne contient un lien vers le profil `Employe` de Paul, les dates choisies, le type choisi, le motif, le statut `en_attente`, et la date de soumission automatique.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
L'application n'aurait aucune structure pour stocker les employés et les demandes. Les vues pourraient afficher des pages, mais elles ne sauraient pas quoi enregistrer dans la base.

### Nom du fichier : conges/admin.py

**Rôle dans l'application :**
Ce fichier rend les modèles `Employe` et `DemandeConge` visibles dans l'admin Django.

**Analogie :**
🧩 L'admin Django est un panneau de contrôle réservé aux techniciens. Les utilisateurs normaux voient le guichet ; l'administrateur voit l'arrière-boutique.

**Explications ligne par ligne (ou bloc par bloc) :**

```python
from django.contrib import admin
from .models import DemandeConge, Employe
```

`admin` vient de Django et permet d'enregistrer des modèles dans l'interface `/admin/`. La ligne suivante importe les deux modèles créés dans `models.py`.

```python
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
```

`@admin.register(Employe)` inscrit le modèle `Employe` dans l'admin. `ModelAdmin` permet de personnaliser son affichage.

```python
list_display = ('user', 'solde_conges')
search_fields = ('user__username',)
```

`list_display` choisit les colonnes visibles dans la liste admin. `search_fields` permet de chercher un employé par username.

```python
@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
```

Ce bloc inscrit les demandes de congé dans l'admin.

```python
list_display = ('employe', 'date_debut', 'date_fin', 'type_conge', 'statut', 'date_soumission')
list_filter = ('statut', 'type_conge')
search_fields = ('employe__user__username', 'motif')
```

L'admin affiche les colonnes utiles, permet de filtrer par statut ou type, et permet de chercher par employé ou motif. `employe__user__username` signifie : va de la demande vers l'employé, puis vers le user, puis vers son username.

**Scénario concret :**
L'administrateur ouvre `http://127.0.0.1:8001/admin/`, se connecte avec `admin / admin123`, puis voit les tables `Employes` et `Demande conges`. Il peut corriger un solde, consulter une demande ou modifier un statut.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Les modèles existeraient encore en base, mais l'administrateur ne les verrait pas dans l'interface admin.

### Nom du fichier : conges/forms.py

**Rôle dans l'application :**
Ce fichier crée le formulaire Django utilisé par l'employé pour soumettre une demande de congé.

**Analogie :**
🧩 Un formulaire Django est comme un formulaire papier intelligent : il sait quelles cases afficher, quelles réponses sont autorisées, et comment transformer le papier rempli en donnée rangée dans le classeur.

**Explications ligne par ligne (ou bloc par bloc) :**

```python
from django import forms
from .models import DemandeConge
```

`forms` est l'outil Django pour créer des formulaires. `DemandeConge` est le modèle utilisé comme source.

```python
class DemandeCongeForm(forms.ModelForm):
```

`ModelForm` signifie : "construis un formulaire à partir d'un modèle". Django lit les champs du modèle et prépare les champs HTML correspondants.

```python
class Meta:
    model = DemandeConge
    fields = ['date_debut', 'date_fin', 'type_conge', 'motif']
```

`Meta` configure le formulaire. `model = DemandeConge` indique le modèle ciblé. `fields` liste les champs que l'employé peut remplir.

Le champ `statut` n'est pas inclus, car l'employé ne doit pas choisir lui-même si sa demande est validée. C'est le responsable qui décide.

```python
widgets = {
    'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    'type_conge': forms.Select(attrs={'class': 'form-select'}),
    'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
}
```

Les **widgets** contrôlent l'apparence HTML des champs. `DateInput` avec `type='date'` donne un sélecteur de date. `Select` donne une liste déroulante. `Textarea` donne une grande zone de texte. Les classes `form-control` et `form-select` viennent de Bootstrap et donnent un style propre.

**Scénario concret :**
Quand Paul ouvre `/soumettre/`, la vue crée `DemandeCongeForm`. Le template affiche les champs. Quand Paul clique sur envoyer, le formulaire vérifie que les dates et le type ressemblent à des données valides avant que Django enregistre la demande.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
La page de soumission ne saurait pas quels champs afficher ou comment valider proprement les données envoyées.

### Nom du fichier : conges/urls.py + config/urls.py

**Rôle dans l'application :**
Ces fichiers relient les adresses tapées dans le navigateur aux vues Python qui doivent répondre.

**Analogie :**
🧩 Le système d'URL est un panneau de signalisation dans une ville. Si tu prends la rue `/login/`, tu arrives au bureau de connexion. Si tu prends `/responsable/`, tu arrives au bureau du responsable.

**Explications ligne par ligne (ou bloc par bloc) :**

Dans `config/urls.py` :

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('conges.urls')),
    path('admin/', admin.site.urls),
]
```

`path` crée une route. `include('conges.urls')` délègue toutes les routes de la racine à `conges/urls.py`. `admin.site.urls` branche l'admin Django sur `/admin/`.

🧩 Analogie : le fichier principal est un chef d'accueil. Il dit : "Pour les pages normales, allez voir l'équipe conges ; pour l'administration, allez au bureau admin."

Dans `conges/urls.py` :

```python
from django.urls import path
from . import views

app_name = 'conges'
```

On importe `path`, puis les vues. `app_name = 'conges'` donne un nom de famille aux routes. Cela permet d'écrire `{% url 'conges:login' %}` sans confusion.

```python
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('employe/', views.employe_home, name='employe_home'),
    path('soumettre/', views.soumettre_demande, name='soumettre_demande'),
    path('responsable/', views.responsable_home, name='responsable_home'),
    path('traiter/<int:demande_id>/', views.traiter_demande, name='traiter_demande'),
]
```

Chaque ligne associe une URL à une fonction dans `views.py`. `<int:demande_id>` signifie que Django capture un nombre dans l'URL, par exemple `/traiter/3/`, et le donne à la vue sous le nom `demande_id`.

| URL | Vue appelée | Ce que l'utilisateur voit |
|---|---|---|
| `/` | `dashboard_view` | Redirection vers employé ou responsable |
| `/login/` | `login_view` | Formulaire de connexion |
| `/logout/` | `logout_view` | Déconnexion puis retour au login |
| `/employe/` | `employe_home` | Solde et historique de l'employé |
| `/soumettre/` | `soumettre_demande` | Formulaire de demande de congé |
| `/responsable/` | `responsable_home` | Tableau des demandes en attente |
| `/traiter/<id>/` | `traiter_demande` | Traitement d'une demande puis redirection |
| `/admin/` | `admin.site.urls` | Interface admin Django |

**Scénario concret :**
Paul tape `/soumettre/`. `config/urls.py` délègue à `conges/urls.py`. `conges/urls.py` trouve la route `soumettre/` et appelle `soumettre_demande` dans `views.py`.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Le navigateur demanderait des pages, mais Django ne saurait pas quelle fonction appeler. L'utilisateur verrait des erreurs 404.

### Nom du fichier : conges/views.py

**Rôle dans l'application :**
Ce fichier contient la logique des pages : connexion, déconnexion, tableau employé, soumission et validation des demandes.

**Analogie :**
🧩 Une vue Django est comme une personne à un guichet. Elle reçoit une demande, regarde les papiers, consulte les dossiers, puis répond avec une page ou envoie la personne vers un autre guichet.

**Explications ligne par ligne (ou bloc par bloc) :**

`request` est l'objet qui représente la demande du navigateur. 🧩 C'est une enveloppe : elle contient qui demande, quelle URL est appelée, quelle méthode est utilisée, et les données du formulaire.

`GET` veut dire : "je veux voir une page". 🧩 C'est regarder une vitrine. `POST` veut dire : "j'envoie des données pour changer quelque chose". 🧩 C'est passer une commande au comptoir.

```python
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
```

`messages` affiche des petits retours utilisateur. `authenticate` vérifie les identifiants. `login` connecte l'utilisateur. `logout` le déconnecte. `login_required` protège une vue. `AuthenticationForm` est le formulaire de connexion Django. `render` fabrique une page HTML avec un template. `redirect` renvoie vers une autre URL. `get_object_or_404` cherche un objet et affiche une erreur 404 s'il n'existe pas.

```python
from .forms import DemandeCongeForm
from .models import DemandeConge, Employe
```

La vue importe le formulaire de demande et les modèles nécessaires pour lire et écrire dans la base.

#### Vue `login_view`

```python
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('conges:dashboard')
        messages.error(request, 'Identifiants incorrects.')

    return render(request, 'conges/login.html', {'form': form})
```

Cette fonction se déclenche quand l'utilisateur va sur `/login/`. Elle reçoit `request`. En GET, elle affiche le formulaire. En POST, elle lit `username` et `password`, puis demande à Django si ces identifiants sont bons.

Si `authenticate` trouve un utilisateur, `login` ouvre la session, puis `redirect` envoie vers le dashboard. Sinon, un message d'erreur est affiché.

🎯 Scénario humain : Paul arrive sur la page de connexion. La vue lui donne un formulaire. Il écrit `employe1` et `employe123`. La vue vérifie dans la base, connecte Paul, puis l'envoie vers `/`.

#### Vue `logout_view`

```python
@login_required
def logout_view(request):
    logout(request)
    return redirect('conges:login')
```

Cette fonction se déclenche quand l'utilisateur clique sur "Déconnexion". `@login_required` signifie qu'il faut être connecté pour l'utiliser. Elle ferme la session avec `logout`, puis renvoie vers la connexion.

🎯 Scénario humain : Paul clique sur Déconnexion. Django efface son badge d'accès, puis le ramène à l'entrée.

#### Vue `dashboard_view`

```python
@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect('conges:responsable_home')
    return redirect('conges:employe_home')
```

Cette fonction se déclenche quand l'utilisateur va sur `/`. Elle regarde `request.user.is_staff`. Dans ce projet simple, `is_staff=True` signifie responsable ou administrateur. Si oui, Django redirige vers `/responsable/`. Sinon, vers `/employe/`.

🎯 Scénario humain : Marie, responsable, arrive à l'accueil. Le guichet voit son badge staff et l'envoie au bureau de validation. Paul n'a pas ce badge, donc il va à son espace employé.

#### Vue `employe_home`

```python
@login_required
def employe_home(request):
    employe, created = Employe.objects.get_or_create(user=request.user)
    demandes = DemandeConge.objects.filter(employe=employe).order_by('-date_soumission')
    context = {'employe': employe, 'demandes': demandes, 'created': created}
    return render(request, 'conges/employe_home.html', context)
```

Cette fonction se déclenche sur `/employe/`. `get_or_create` cherche le profil `Employe` lié à l'utilisateur connecté ; s'il n'existe pas, il le crée. `filter` crée un **QuerySet**, c'est-à-dire une liste de résultats venant de la base. `order_by('-date_soumission')` trie du plus récent au plus ancien.

`context` est le sac de données envoyé au template : l'employé, ses demandes et l'information `created`. `render` utilise `employe_home.html`.

🎯 Scénario humain : Paul ouvre son espace. La vue retrouve sa fiche employé, rassemble toutes ses demandes, puis donne le paquet au template pour afficher un tableau.

#### Vue `soumettre_demande`

```python
@login_required
def soumettre_demande(request):
    employe, created = Employe.objects.get_or_create(user=request.user)
    form = DemandeCongeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        demande = form.save(commit=False)
        demande.employe = employe
        demande.save()
        messages.success(request, 'Votre demande a été soumise.')
        return redirect('conges:employe_home')

    return render(request, 'conges/soumettre_demande.html', {'form': form})
```

Cette fonction se déclenche sur `/soumettre/`. En GET, elle affiche un formulaire vide. En POST, elle vérifie `form.is_valid()`. Si les données sont correctes, `form.save(commit=False)` prépare l'objet sans l'enregistrer tout de suite. C'est nécessaire pour ajouter `demande.employe = employe`. Ensuite `demande.save()` écrit la ligne en base.

🎯 Scénario humain : Paul remplit le formulaire. La vue vérifie que les cases sont correctes, colle l'étiquette "demande de Paul" sur le dossier, range le dossier dans le classeur, puis ramène Paul à son historique.

#### Vue `responsable_home`

```python
@login_required
def responsable_home(request):
    if not request.user.is_staff:
        return redirect('conges:employe_home')
    demandes = DemandeConge.objects.filter(statut='en_attente').order_by('date_soumission')
    return render(request, 'conges/responsable_home.html', {'demandes': demandes})
```

Cette fonction se déclenche sur `/responsable/`. Elle vérifie que l'utilisateur est staff. Si ce n'est pas le cas, elle renvoie vers l'espace employé. Sinon, elle cherche toutes les demandes avec `statut='en_attente'`, triées de la plus ancienne à la plus récente.

🎯 Scénario humain : Marie ouvre son espace. La vue vérifie son badge responsable, sort la pile des demandes non traitées, puis affiche le tableau.

#### Vue `traiter_demande`

```python
@login_required
def traiter_demande(request, demande_id):
    if not request.user.is_staff:
        return redirect('conges:employe_home')
    demande = get_object_or_404(DemandeConge, id=demande_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'valider':
            demande.statut = 'validee'
            messages.success(request, 'La demande a été validée.')
        elif action == 'refuser':
            demande.statut = 'refusee'
            messages.warning(request, 'La demande a été refusée.')
        demande.save()

    return redirect('conges:responsable_home')
```

Cette fonction se déclenche quand Marie clique sur "Valider" ou "Refuser". Elle reçoit `demande_id`, le numéro de la demande dans l'URL. `get_object_or_404` récupère la demande ou affiche une erreur si elle n'existe pas. Ensuite, la vue lit `action` dans le formulaire POST : `valider` ou `refuser`.

🎯 Scénario humain : Marie clique sur "Valider" pour la demande numéro 3. La vue prend le dossier 3, écrit "Validée" dessus, sauvegarde, puis ramène Marie à la pile des demandes restantes.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Les URLs pointeraient vers des fonctions absentes ou cassées. Les utilisateurs verraient des erreurs, ne pourraient pas se connecter, soumettre ou traiter les demandes.

### Nom du fichier : conges/templates/conges/base.html

**Rôle dans l'application :**
Ce template est la structure commune de toutes les pages : Bootstrap, navbar, messages et zone de contenu.

**Analogie :**
🧩 `base.html`, c'est le cadre d'une maison : murs, entrée, couloir et éclairage. Les autres templates aménagent les pièces à l'intérieur.

**Explications ligne par ligne (ou bloc par bloc) :**

```html
<!doctype html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Gestion des congés</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
```

Cette partie prépare la page HTML. Le CDN Bootstrap charge le style depuis Internet. Un **CDN** est un serveur public qui distribue des fichiers, comme une bibliothèque municipale qui prête le même livre à beaucoup de gens.

```html
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
```

`bg-light`, `navbar`, `navbar-dark`, `bg-primary` sont des classes Bootstrap. Elles donnent un fond clair au site et une barre de navigation bleue.

```html
<a class="navbar-brand" href="{% url 'conges:dashboard' %}">Congés</a>
```

`{% url 'conges:dashboard' %}` est une balise Django qui fabrique l'URL à partir du nom de route. Cela évite d'écrire `/` à la main.

```html
{% if user.is_authenticated %}
    <span>{{ user.username }}</span>
    <a class="btn btn-sm btn-outline-light" href="{% url 'conges:logout' %}">Déconnexion</a>
{% endif %}
```

`{% if %}` teste une condition. `{{ user.username }}` affiche une variable. Ici, si l'utilisateur est connecté, on affiche son nom et le bouton de déconnexion.

```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} mb-3">{{ message }}</div>
    {% endfor %}
{% endif %}
```

`{% for %}` répète un morceau de HTML pour chaque message. `alert-{{ message.tags }}` adapte la couleur Bootstrap selon le type de message.

```html
{% block content %}{% endblock %}
```

`{% block %}` crée une zone remplaçable. Les templates enfants utilisent `{% extends 'conges/base.html' %}` pour reprendre toute la structure et remplir seulement ce bloc.

**Scénario concret :**
Quand Paul ouvre n'importe quelle page, `base.html` fournit le décor commun : barre bleue, nom de l'utilisateur, bouton déconnexion et emplacement central pour le contenu de la page.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Les autres templates qui font `{% extends 'conges/base.html' %}` ne pourraient plus s'afficher correctement.

### Nom du fichier : conges/templates/conges/login.html

**Rôle dans l'application :**
Ce template affiche le formulaire de connexion.

**Analogie :**
🧩 C'est le comptoir d'accueil : on présente sa carte d'identité avant d'entrer.

**Explications ligne par ligne (ou bloc par bloc) :**

```html
{% extends 'conges/base.html' %}

{% block content %}
```

Le template hérite de `base.html` et remplit son bloc `content`.

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary w-100" type="submit">Se connecter</button>
</form>
```

`method="post"` envoie les identifiants au serveur. `{% csrf_token %}` ajoute un jeton de sécurité pour prouver que le formulaire vient bien du site. `{{ form.as_p }}` affiche le formulaire Django en paragraphes HTML. `btn btn-primary w-100` crée un bouton Bootstrap bleu qui prend toute la largeur.

**Scénario concret :**
La vue `login_view` prépare `form`, le met dans le contexte, et `login.html` le sert joliment à Paul. Paul remplit et clique sur "Se connecter".

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
La page `/login/` ne pourrait pas afficher le formulaire de connexion.

### Nom du fichier : conges/templates/conges/employe_home.html

**Rôle dans l'application :**
Ce template affiche l'espace employé avec le solde et l'historique des demandes.

**Analogie :**
🧩 C'est le tableau d'affichage personnel de Paul : ses jours disponibles et ses dossiers déjà envoyés.

**Explications ligne par ligne (ou bloc par bloc) :**

```html
{% extends 'conges/base.html' %}
{% block content %}
```

La page reprend la structure commune puis remplit le contenu.

```html
<a class="btn btn-primary" href="{% url 'conges:soumettre_demande' %}">Nouvelle demande</a>
```

Ce bouton envoie vers la route nommée `soumettre_demande`.

```html
<p class="mb-0 fs-5">Solde de congés : <strong>{{ employe.solde_conges }} jours</strong></p>
```

`{{ employe.solde_conges }}` affiche la valeur passée par la vue. La vue prépare le plateau, le template le présente.

```html
{% for demande in demandes %}
    <tr>
        <td>{{ demande.date_debut }}</td>
        <td>{{ demande.date_fin }}</td>
        <td>{{ demande.get_type_conge_display }}</td>
        <td>{{ demande.motif|default:"-" }}</td>
```

La boucle parcourt toutes les demandes de l'employé. `get_type_conge_display` affiche le libellé humain du choix, par exemple "Congé annuel". `default:"-"` affiche un tiret si le motif est vide.

```html
{% if demande.statut == 'validee' %}
    <span class="badge text-bg-success">{{ demande.get_statut_display }}</span>
{% elif demande.statut == 'refusee' %}
    <span class="badge text-bg-danger">{{ demande.get_statut_display }}</span>
{% else %}
    <span class="badge text-bg-warning">{{ demande.get_statut_display }}</span>
{% endif %}
```

Le statut est coloré : vert pour validée, rouge pour refusée, jaune pour en attente. `badge`, `text-bg-success`, `text-bg-danger`, `text-bg-warning` sont des classes Bootstrap.

```html
{% empty %}
    <tr>
        <td colspan="5" class="text-center text-muted">Aucune demande pour le moment.</td>
    </tr>
{% endfor %}
```

`{% empty %}` s'affiche si la boucle n'a aucun élément.

**Scénario concret :**
Paul arrive sur `/employe/`. La vue lui donne `employe` et `demandes`. Le template affiche son solde en haut, puis une ligne par demande.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
L'employé ne verrait ni son solde ni son historique.

### Nom du fichier : conges/templates/conges/soumettre_demande.html

**Rôle dans l'application :**
Ce template affiche le formulaire de création d'une demande de congé.

**Analogie :**
🧩 C'est le formulaire papier posé sur le bureau RH, avec les cases "date de début", "date de fin", "type" et "motif".

**Explications ligne par ligne (ou bloc par bloc) :**

```html
<a class="btn btn-link px-0 mb-3" href="{% url 'conges:employe_home' %}">Retour</a>
```

Ce lien permet de revenir à l'espace employé.

```html
<form method="post">
    {% csrf_token %}
    {{ form.non_field_errors }}
```

Le formulaire envoie une demande en POST. Le jeton CSRF protège l'envoi. `form.non_field_errors` affiche les erreurs générales du formulaire.

```html
<label class="form-label" for="{{ form.date_debut.id_for_label }}">Date de début</label>
{{ form.date_debut }}
{{ form.date_debut.errors }}
```

Chaque champ est affiché avec son label, son widget et ses erreurs éventuelles. `id_for_label` relie le label au champ HTML.

```html
{{ form.date_fin }}
{{ form.type_conge }}
{{ form.motif }}
```

Ces champs viennent du `DemandeCongeForm`. La vue ne transmet pas chaque champ séparément ; elle transmet le formulaire complet.

```html
<button class="btn btn-primary" type="submit">Envoyer la demande</button>
```

Le bouton envoie le formulaire à la vue `soumettre_demande`.

**Scénario concret :**
Paul choisit ses dates, sélectionne "Congé annuel", écrit "Vacances familiales", puis clique sur envoyer. Le navigateur envoie ces données à la vue.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Paul ne pourrait pas saisir une nouvelle demande dans l'interface.

### Nom du fichier : conges/templates/conges/responsable_home.html

**Rôle dans l'application :**
Ce template affiche les demandes en attente et les boutons pour valider ou refuser.

**Analogie :**
🧩 C'est la pile de dossiers sur le bureau de Marie, avec deux tampons à côté : "Validé" et "Refusé".

**Explications ligne par ligne (ou bloc par bloc) :**

```html
{% for demande in demandes %}
    <tr>
        <td>{{ demande.employe.user.username }}</td>
        <td>{{ demande.date_debut }}</td>
        <td>{{ demande.date_fin }}</td>
        <td>{{ demande.get_type_conge_display }}</td>
        <td>{{ demande.motif|default:"-" }}</td>
```

La boucle affiche chaque demande en attente transmise par `responsable_home`. Elle montre le nom de l'employé, les dates, le type et le motif.

```html
<form method="post" action="{% url 'conges:traiter_demande' demande.id %}">
    {% csrf_token %}
    <button class="btn btn-success btn-sm" name="action" value="valider" type="submit">Valider</button>
</form>
```

Ce formulaire envoie une action `valider` à la route `traiter_demande` pour la demande concernée.

```html
<form method="post" action="{% url 'conges:traiter_demande' demande.id %}">
    {% csrf_token %}
    <button class="btn btn-danger btn-sm" name="action" value="refuser" type="submit">Refuser</button>
</form>
```

Ce formulaire envoie une action `refuser`. Les classes Bootstrap donnent un bouton vert pour valider et rouge pour refuser.

```html
{% empty %}
    <tr>
        <td colspan="6" class="text-center text-muted">Aucune demande en attente.</td>
    </tr>
{% endfor %}
```

Si aucune demande n'attend de décision, le tableau affiche un message clair.

**Scénario concret :**
Marie ouvre `/responsable/`. Elle voit la demande de Paul. Elle clique sur "Valider". Le formulaire POST appelle `traiter_demande`, qui change le statut.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Le responsable ne pourrait pas voir la file d'attente ni traiter les demandes depuis l'interface.

### Nom du fichier : init_data.py

**Rôle dans l'application :**
Ce script crée les comptes de test nécessaires pour essayer l'application rapidement.

**Analogie :**
🧩 C'est comme préparer une salle de classe avant un exercice : on pose déjà trois badges sur la table, un pour l'administrateur, un pour l'employé, un pour le responsable.

**Explications ligne par ligne (ou bloc par bloc) :**

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
```

Un script externe ne démarre pas automatiquement Django comme `manage.py`. Il faut donc dire où sont les réglages, puis appeler `django.setup()`. Cela charge les modèles et la configuration.

```python
from django.contrib.auth.models import User
from conges.models import Employe
```

Ces imports viennent après `django.setup()` pour que Django soit prêt. `User` sert à créer les comptes, `Employe` sert à créer les profils congés.

```python
def create_user(username, password, is_staff=False, is_superuser=False):
    user, created = User.objects.get_or_create(username=username)
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.set_password(password)
    user.save()
    return user
```

Cette fonction crée ou récupère un utilisateur. `get_or_create` évite les doublons. `is_staff` donne accès au rôle responsable et à l'admin. `is_superuser` donne tous les droits admin. `set_password` chiffre le mot de passe correctement.

```python
admin_user = create_user('admin', 'admin123', is_staff=True, is_superuser=True)
employe_user = create_user('employe1', 'employe123')
responsable_user = create_user('responsable1', 'responsable123', is_staff=True)
```

Trois utilisateurs sont créés :

- `admin / admin123` : administrateur complet.
- `employe1 / employe123` : employé simple.
- `responsable1 / responsable123` : responsable, grâce à `is_staff=True`.

```python
Employe.objects.get_or_create(user=employe_user, defaults={'solde_conges': 25})
Employe.objects.get_or_create(user=responsable_user, defaults={'solde_conges': 25})
```

Ces lignes créent les profils congés pour l'employé et le responsable. Le responsable peut aussi avoir un profil, même si son rôle principal est de valider.

Pour relancer ce script :

```bash
.venv/bin/python init_data.py
```

**Scénario concret :**
Tu récupères le projet sur une nouvelle machine. Avant de tester, tu lances `init_data.py`. Les comptes de démonstration sont prêts et tu peux te connecter tout de suite.

**Ce qui se passerait si ce fichier n'existait pas ou était mal écrit :**
Il faudrait créer les comptes à la main dans l'admin ou avec `createsuperuser`, ce qui serait plus long pour tester.

---

## Partie 3 – Comment tout ça s'assemble : le voyage d'une demande de congé

Paul ouvre son navigateur et va sur `http://127.0.0.1:8001/login/`. Le fichier `config/urls.py` reçoit l'adresse et délègue à `conges/urls.py`, parce que la route principale inclut toutes les routes de l'application `conges`.

Dans `conges/urls.py`, Django trouve :

```python
path('login/', views.login_view, name='login')
```

Il appelle donc `login_view` dans `conges/views.py`. Comme Paul arrive simplement pour voir la page, la requête est en GET. La vue crée un `AuthenticationForm`, puis utilise `render` pour afficher `conges/templates/conges/login.html`.

Le template `login.html` hérite de `base.html`. `base.html` fournit la barre de navigation, Bootstrap et la zone centrale. `login.html` remplit cette zone avec le formulaire de connexion. Paul tape `employe1` et `employe123`, puis clique sur "Se connecter".

Cette fois, le navigateur envoie une requête POST à la même URL. `login_view` lit `request.POST`, récupère `username` et `password`, puis appelle `authenticate`. Django vérifie ces informations dans `db.sqlite3`, où les comptes ont été créés par `init_data.py`. Comme les identifiants sont corrects, `login(request, user)` ouvre la session de Paul.

La vue renvoie ensuite :

```python
return redirect('conges:dashboard')
```

Django va donc sur `/`. Dans `conges/urls.py`, `/` appelle `dashboard_view`. Cette vue regarde `request.user.is_staff`. Paul n'est pas staff, donc elle le redirige vers `employe_home`, c'est-à-dire `/employe/`.

Dans `employe_home`, Django récupère ou crée le profil `Employe` de Paul :

```python
employe, created = Employe.objects.get_or_create(user=request.user)
```

Puis il cherche les demandes de Paul :

```python
demandes = DemandeConge.objects.filter(employe=employe).order_by('-date_soumission')
```

La vue prépare un contexte avec `employe` et `demandes`, puis affiche `employe_home.html`. Le template montre le solde de Paul et son historique. Paul clique sur "Nouvelle demande".

Le bouton utilise :

```html
{% url 'conges:soumettre_demande' %}
```

Django fabrique l'URL `/soumettre/`. Cette URL appelle `soumettre_demande` dans `views.py`. En GET, la vue prépare un `DemandeCongeForm` vide et affiche `soumettre_demande.html`.

Paul remplit le formulaire : date de début, date de fin, type de congé et motif. Quand il clique sur "Envoyer la demande", le navigateur envoie un POST. La vue vérifie :

```python
if request.method == 'POST' and form.is_valid():
```

Si le formulaire est valide, Django prépare la demande sans encore l'enregistrer :

```python
demande = form.save(commit=False)
```

Puis il colle l'étiquette de Paul sur la demande :

```python
demande.employe = employe
```

Ensuite, `demande.save()` crée une ligne dans `db.sqlite3`. Le modèle `DemandeConge` donne automatiquement le statut `en_attente` et remplit `date_soumission`. Paul est redirigé vers `/employe/`, où il voit sa demande en jaune avec le statut "En attente".

Marie, la responsable, ouvre `http://127.0.0.1:8001/login/`. Elle se connecte avec `responsable1 / responsable123`. `login_view` l'authentifie, puis l'envoie vers le dashboard. Cette fois, `dashboard_view` voit :

```python
if request.user.is_staff:
```

Marie est staff, donc Django la redirige vers `/responsable/`.

La vue `responsable_home` vérifie encore que Marie est staff, puis cherche toutes les demandes en attente :

```python
demandes = DemandeConge.objects.filter(statut='en_attente').order_by('date_soumission')
```

Elle affiche `responsable_home.html`. Le template montre un tableau avec la demande de Paul et deux boutons : "Valider" et "Refuser".

Marie clique sur "Valider". Le formulaire POST appelle une URL du type `/traiter/1/`, où `1` est l'identifiant de la demande. `conges/urls.py` capture ce nombre grâce à :

```python
path('traiter/<int:demande_id>/', views.traiter_demande, name='traiter_demande')
```

La vue `traiter_demande` reçoit `demande_id`, retrouve la demande avec `get_object_or_404`, lit `action='valider'`, puis change :

```python
demande.statut = 'validee'
demande.save()
```

La demande est maintenant validée dans la base. Marie revient sur la liste des demandes en attente. Comme la demande de Paul n'est plus `en_attente`, elle disparaît de cette file.

Paul revient sur son espace employé. `employe_home` recharge ses demandes depuis la base. `employe_home.html` affiche maintenant le statut "Validée" en vert. Dans le code actuel, le solde affiché reste à 25, car aucune ligne ne retire encore des jours du champ `solde_conges`.

---

## Partie 4 – Vocabulaire Django : le mini-glossaire

**Model** : Classe Python qui décrit une table de base de données. 🧩 Comme un formulaire officiel à remplir.

**View** : Fonction qui reçoit une requête et renvoie une réponse. 🧩 Comme un guichetier.

**Template** : Fichier HTML qui affiche les données joliment. 🧩 Comme une vitrine de magasin.

**URL** : Adresse dans le navigateur reliée à une vue. 🧩 Comme une rue sur un plan de ville.

**Migration** : Instruction pour créer ou modifier la base. 🧩 Comme un plan de construction.

**QuerySet** : Liste de résultats venant de la base de données. 🧩 Comme une pile de fiches trouvées dans un classeur.

**ForeignKey** : Lien entre deux tables. 🧩 Comme une facture liée à son client.

**CharField** : Champ texte court. 🧩 Comme une petite case "nom".

**DateField** : Champ qui stocke une date. 🧩 Comme une case de calendrier.

**IntegerField** : Champ qui stocke un nombre entier. 🧩 Comme un compteur.

**choices** : Liste de valeurs autorisées. 🧩 Comme un menu déroulant.

**ModelForm** : Formulaire construit à partir d'un modèle. 🧩 Comme un formulaire papier déjà aligné avec le classeur.

**render** : Fonction qui combine une vue, un template et des données pour produire une page. 🧩 Comme dresser une assiette.

**redirect** : Fonction qui envoie l'utilisateur vers une autre page. 🧩 Comme indiquer un autre guichet.

**request** : Objet qui contient la demande du navigateur. 🧩 Comme une enveloppe avec l'adresse et les documents.

**GET** : Méthode pour demander à voir une page. 🧩 Comme regarder une vitrine.

**POST** : Méthode pour envoyer des données. 🧩 Comme déposer un dossier signé.

**login_required** : Protection qui exige une connexion. 🧩 Comme un vigile à l'entrée.

**authenticate** : Fonction qui vérifie username et mot de passe. 🧩 Comme contrôler une carte d'identité.

**login** : Fonction qui connecte l'utilisateur. 🧩 Comme donner un badge d'accès.

**logout** : Fonction qui déconnecte l'utilisateur. 🧩 Comme rendre son badge.

**superuser** : Administrateur avec tous les droits. 🧩 Comme le directeur qui a toutes les clés.

**admin** : Interface Django de gestion interne. 🧩 Comme un panneau de contrôle technique.

**INSTALLED_APPS** : Liste des applications activées. 🧩 Comme la liste des pièces branchées à l'électricité.

**{% block %}** : Zone remplaçable dans un template. 🧩 Comme une pièce vide à aménager.

**{% extends %}** : Instruction pour hériter d'un template de base. 🧩 Comme construire une pièce dans une maison déjà bâtie.

**{{ variable }}** : Affiche une donnée dans le HTML. 🧩 Comme coller une étiquette avec une valeur.

**{% for %}** : Répète un bloc pour chaque élément d'une liste. 🧩 Comme distribuer une fiche à chaque personne.

**{% if %}** : Affiche selon une condition. 🧩 Comme choisir une porte selon la couleur du badge.

**{% csrf_token %}** : Jeton de sécurité pour les formulaires POST. 🧩 Comme un bracelet officiel à l'entrée d'un événement.

**CDN** : Serveur public qui fournit un fichier comme Bootstrap. 🧩 Comme une bibliothèque partagée.

**Bootstrap** : Kit CSS pour rendre les pages propres rapidement. 🧩 Comme une boîte de décorations déjà prêtes.

**runserver** : Commande qui lance le serveur local. 🧩 Comme ouvrir la boutique pour les tests.

**makemigrations** : Commande qui prépare les plans de base de données. 🧩 Comme dessiner le plan avant les travaux.

**migrate** : Commande qui applique les plans dans la base. 🧩 Comme construire réellement les murs.

**__str__** : Méthode qui dit comment afficher un objet en texte. 🧩 Comme écrire un nom lisible sur une boîte.

**settings.py** : Fichier de configuration du projet. 🧩 Comme le tableau électrique.

**SQLite** : Base de données simple dans un fichier. 🧩 Comme un classeur Excel portable.

**django.setup()** : Fonction qui initialise Django dans un script externe. 🧩 Comme allumer l'atelier avant d'utiliser les machines.

---

## Partie 5 – Comment relancer le projet depuis zéro sur une nouvelle machine

> Dans ce projet actuel, Django est déjà installé dans `.venv`. Sur une nouvelle machine, voici les étapes propres.

```bash
python -m venv .venv
```

Crée un environnement virtuel, c'est-à-dire une petite boîte Python séparée pour ce projet.

```bash
source .venv/bin/activate
```

Active cette boîte Python sur Linux/macOS.

```bash
pip install Django
```

Installe Django dans l'environnement virtuel.

```bash
python manage.py migrate
```

Crée les tables nécessaires dans `db.sqlite3` à partir des migrations.

```bash
python init_data.py
```

Crée ou met à jour les comptes de test : admin, employé et responsable.

```bash
python manage.py runserver
```

Lance le serveur local, généralement sur `http://127.0.0.1:8000/`.

Comptes à utiliser :

- Admin : `admin / admin123`, à ouvrir sur `/admin/`
- Employé : `employe1 / employe123`, à ouvrir sur `/login/`
- Responsable : `responsable1 / responsable123`, à ouvrir sur `/login/`

Si le port 8000 est déjà utilisé :

```bash
python manage.py runserver 127.0.0.1:8001
```

Cette commande lance le site sur le port 8001.

---

## Partie 6 – Et si tu devais tout reconstruire seul ?

✅ Checklist pour reconstruire le projet identique de zéro.

### Préparer le projet

- Crée un environnement virtuel avec `python -m venv .venv`.
- Active l'environnement virtuel avec `source .venv/bin/activate`.
- Installe Django avec `pip install Django`.
- Crée un projet Django si nécessaire avec `django-admin startproject config .`.
- Lance `python manage.py startapp conges`.

### Configurer `config/settings.py`

- Ajoute `'conges'` dans `INSTALLED_APPS`.
- Vérifie que `DATABASES` utilise SQLite avec `db.sqlite3`.
- Ajoute `LOGIN_URL = 'conges:login'`.
- Mets `ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']` pour le local et les tests.

### Écrire `conges/models.py`

- Importe `User` depuis `django.contrib.auth.models`.
- Importe `models` depuis `django.db`.
- Crée le modèle `Employe` avec `user = OneToOneField(User)` et `solde_conges = IntegerField(default=25)`.
- Ajoute `__str__` pour afficher le username.
- Crée le modèle `DemandeConge`.
- Ajoute `TYPE_CHOICES` pour annuel, maladie et autre.
- Ajoute `STATUT_CHOICES` pour en attente, validée et refusée.
- Ajoute les champs `employe`, `date_debut`, `date_fin`, `type_conge`, `motif`, `statut`, `date_soumission`.
- Ajoute `__str__` pour afficher l'employé et les dates.

### Créer la base

- Lance `python manage.py makemigrations conges`.
- Lance `python manage.py migrate`.

### Écrire `conges/admin.py`

- Importe `admin`.
- Importe `Employe` et `DemandeConge`.
- Enregistre `Employe` avec `@admin.register`.
- Configure `list_display` et `search_fields`.
- Enregistre `DemandeConge` avec `@admin.register`.
- Configure `list_display`, `list_filter` et `search_fields`.

### Écrire `conges/forms.py`

- Importe `forms`.
- Importe `DemandeConge`.
- Crée `DemandeCongeForm(forms.ModelForm)`.
- Dans `Meta`, indique `model = DemandeConge`.
- Mets les champs `date_debut`, `date_fin`, `type_conge`, `motif`.
- Ajoute les widgets Bootstrap pour les dates, la liste déroulante et le motif.

### Écrire `conges/views.py`

- Importe `messages`, `authenticate`, `login`, `logout`, `login_required`, `AuthenticationForm`, `get_object_or_404`, `redirect`, `render`.
- Importe `DemandeCongeForm`, `DemandeConge` et `Employe`.
- Écris `login_view` pour afficher et traiter la connexion.
- Écris `logout_view` pour déconnecter.
- Écris `dashboard_view` pour rediriger selon `is_staff`.
- Écris `employe_home` pour afficher solde et historique.
- Écris `soumettre_demande` pour créer une demande.
- Écris `responsable_home` pour afficher les demandes en attente.
- Écris `traiter_demande` pour valider ou refuser.

### Écrire les URLs

- Crée `conges/urls.py`.
- Ajoute `app_name = 'conges'`.
- Ajoute les routes `/`, `/login/`, `/logout/`, `/employe/`, `/soumettre/`, `/responsable/`, `/traiter/<int:demande_id>/`.
- Dans `config/urls.py`, importe `include`.
- Ajoute `path('', include('conges.urls'))`.
- Garde `path('admin/', admin.site.urls)`.

### Écrire les templates

- Crée le dossier `conges/templates/conges/`.
- Écris `base.html` avec Bootstrap CDN, navbar, messages et `{% block content %}`.
- Écris `login.html` avec `{% extends %}`, `{% csrf_token %}` et `{{ form.as_p }}`.
- Écris `employe_home.html` avec solde, historique, boucle `{% for %}` et badges de statut.
- Écris `soumettre_demande.html` avec les champs du formulaire.
- Écris `responsable_home.html` avec le tableau des demandes et les boutons Valider/Refuser.

### Écrire `init_data.py`

- Configure `DJANGO_SETTINGS_MODULE`.
- Appelle `django.setup()`.
- Importe `User` et `Employe`.
- Écris une fonction `create_user`.
- Crée `admin`, `employe1` et `responsable1`.
- Crée les profils `Employe` nécessaires.

### Vérifier et lancer

- Lance `python manage.py check`.
- Lance `python init_data.py`.
- Lance `python manage.py runserver`.
- Ouvre `/login/`.
- Teste le compte employé.
- Soumets une demande.
- Teste le compte responsable.
- Valide ou refuse la demande.
- Ouvre `/admin/` avec le compte admin pour vérifier les données.
