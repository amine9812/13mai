# 1. Project overview
This project is a Django web application for managing employee holiday/leave requests.
- Employees log in, view their leave balance/history, and submit requests.
- Responsible/HR users log in, view pending requests, and approve or refuse them.
- Admin users can manage data through Django Admin at `/admin/`.
Main goal: replace a manual leave request process with a small web system.
Real-life scenario: an employee wants holiday leave, fills a request form, and HR/admin checks it and approves or refuses it.
The active app is `conges` ("leave" in French). The project is a good demo because it shows login, roles, forms, database records, templates, admin, and a complete approval workflow.
Important: this is a demo/local application, not a full production HR platform yet.

# 2. Why Django was used
Django is a Python web framework. A framework is a ready-made toolbox for building web applications faster.
Real-life analogy: Django is like a ready-made building structure. The walls, doors, electricity, and water are already prepared; the developer customizes the rooms.
Why Django fits this project:
| Django feature | How this project uses it |
|---|---|
| Routing/URLs | Maps `/login/`, `/soumettre/`, `/admin/` to code |
| Views | Runs page logic in `conges/views.py` |
| Templates | Shows HTML pages from `conges/templates/conges/` |
| Models/ORM | Stores employees and leave requests |
| Forms | Validates leave request input |
| Admin panel | Gives management UI at `/admin/` |
| Authentication | Uses Django users, login, logout, staff/admin flags |
| CSRF security | Protects POST forms with `{% csrf_token %}` |
Django is faster than scratch because password handling, sessions, database queries, form security, and admin pages already exist.
This project uses Django's built-in `User` model for usernames, passwords, staff status, and superuser status.

# 3. Django architecture explained simply
Django uses MVT: Model, View, Template.
| Part | Simple meaning | Real file example |
|---|---|---|
| Model | Data/database structure | `conges/models.py` |
| View | Logic/controller | `conges/views.py` |
| Template | Visual HTML page | `conges/templates/conges/*.html` |
MVT compared with MVC:
- Model = data.
- Django View = controller/logic.
- Template = visual page.
Real-life analogy:
| Django part | Analogy |
|---|---|
| URL | Road/signpost |
| View | Receptionist/worker who decides what to do |
| Model | Filing cabinet structure |
| Database | Archive/storage room |
| Template | Printed page shown to the user |
Flow:
```text
Browser URL -> urls.py -> view -> model/database if needed -> template -> HTML response
```
Example: `/soumettre/` goes to `soumettre_demande`, which prepares/saves a `DemandeConge` and shows `soumettre_demande.html`.

# 4. Full project structure
Real project tree:
```text
demo_d/
|-- manage.py
|-- db.sqlite3
|-- init_data.py
|-- GUIDE.md
|-- PROJECT_EXPLANATION_GUIDE.md
|-- config/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- conges/
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/0001_initial.py
|   |-- static/conges/styles.css
|   `-- templates/conges/
|       |-- base.html
|       |-- login.html
|       |-- employe_home.html
|       |-- responsable_home.html
|       |-- soumettre_demande.html
|       `-- historique_demandes.html
`-- myapp/
    |-- admin.py
    |-- apps.py
    |-- models.py
    |-- tests.py
    |-- views.py
    `-- migrations/__init__.py
```
Important files:
| File/folder | Used for | Generated or manual? | Why it matters |
|---|---|---|---|
| `manage.py` | Commands | Generated | Runs server, migrations, tests |
| `config/` | Project folder | Generated | Global Django configuration |
| `config/settings.py` | Settings | Generated then edited | Apps, database, templates, static files |
| `config/urls.py` | Main URLs | Generated then edited | Includes `conges.urls` and admin |
| `conges/` | Main app | Generated then developed | Contains HR leave logic |
| `conges/models.py` | Models | Manual code | Defines `Employe`, `DemandeConge` |
| `conges/views.py` | Logic | Manual code | Login, dashboards, submit, approve/refuse |
| `conges/forms.py` | Forms | Manual | Defines `DemandeCongeForm` |
| `conges/admin.py` | Admin setup | Manual code | Shows models in admin |
| `conges/templates/` | HTML pages | Manual | User interface |
| `conges/static/conges/styles.css` | CSS | Manual | Layout, cards, tables, badges |
| `conges/migrations/0001_initial.py` | DB creation | Auto-generated | Creates app tables |
| `conges/tests.py` | Tests | Manual | Tests history visibility |
| `db.sqlite3` | Database | Created by Django | Stores users, employees, requests |
| `init_data.py` | Demo data | Manual | Creates test users |
| `myapp/` | Mostly unused app | Generated | Not in `INSTALLED_APPS` |
The Django project folder is `config`. The active Django app is `conges`. `myapp` exists but is not active in `config/settings.py`.

# 5. How to run the project
There is no `requirements.txt`.
Detected local environment: Python `3.14.3`, Django `6.0.4`.
Windows commands:
```bat
python -m venv venv
venv\Scripts\activate
pip install Django==6.0.4
python manage.py migrate
python init_data.py
python manage.py createsuperuser
python manage.py runserver
```
Linux/Mac commands:
```bash
python3 -m venv venv
source venv/bin/activate
pip install Django==6.0.4
python manage.py migrate
python init_data.py
python manage.py createsuperuser
python manage.py runserver
```
If using the existing `.venv`:
```bash
.venv/bin/python manage.py migrate
.venv/bin/python init_data.py
.venv/bin/python manage.py runserver
```
Open the app: `http://127.0.0.1:8000/`.
Open admin: `http://127.0.0.1:8000/admin/`.
Demo accounts from `init_data.py` and `login.html`:
| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `admin123` |
| Employee | `employe1` | `employe123` |
| Responsible/HR | `responsable1` | `responsable123` |
`python init_data.py` is optional, but useful because it creates these demo accounts.

# 6. Request flow: what happens when a user opens a page
General Django flow:
1. User enters a URL in the browser.
2. Django checks `config/urls.py`.
3. `config/urls.py` includes `conges/urls.py`.
4. `conges/urls.py` calls a view in `conges/views.py`.
5. The view reads/writes models if needed.
6. The view returns HTML with `render()` or redirects with `redirect()`.
7. The browser displays the page.
Real example: submitting leave.
```text
/soumettre/ -> conges/urls.py -> soumettre_demande -> DemandeCongeForm -> DemandeConge -> soumettre_demande.html
```
Actual route:
```python
path('soumettre/', views.soumettre_demande, name='soumettre_demande')
```
Important code:
```python
form = DemandeCongeForm(request.POST or None)
if request.method == 'POST' and form.is_valid():
    demande = form.save(commit=False)
    demande.employe = employe
    demande.save()
    return redirect('conges:employe_home')
```
Meaning: validate the submitted form, create a request, attach the current employee, save it, and return to the employee dashboard.

# 7. Important Django concepts used in this project
## manage.py
`manage.py` is the command center. It runs commands like:
```bash
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py test conges
```
It points Django to `config.settings`. Analogy: it is the remote control for the project.
## settings.py
`config/settings.py` contains configuration. Important real parts:
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
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
LOGIN_URL = 'conges:login'
```
This activates `conges`, uses SQLite, and sends unauthenticated users to login.
## urls.py
`urls.py` is the GPS map from browser address to view. `config/urls.py` includes:
```python
path('', include('conges.urls'))
path('admin/', admin.site.urls)
```
Real routes:
| URL | View |
|---|---|
| `/` | `dashboard_view` |
| `/login/` | `login_view` |
| `/logout/` | `logout_view` |
| `/employe/` | `employe_home` |
| `/historique/` | `historique_demandes` |
| `/soumettre/` | `soumettre_demande` |
| `/responsable/` | `responsable_home` |
| `/traiter/<int:demande_id>/` | `traiter_demande` |
| `/admin/` | Django admin |
## views.py
`conges/views.py` contains function-based views. A view receives `request` and returns a response.
```python
@login_required
def employe_home(request):
    employe, created = Employe.objects.get_or_create(user=request.user)
    demandes = DemandeConge.objects.filter(employe=employe)
```
This creates/fetches the employee profile and lists only that employee's requests.
## render()
`render()` combines request, template, and data:
```python
return render(request, 'conges/login.html', {'form': form})
```
## redirect()
`redirect()` sends the user to another page:
```python
return redirect('conges:dashboard')
```
## models.py
`conges/models.py` defines database tables. `Employe`:
```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
solde_conges = models.IntegerField(default=25)
```
`DemandeConge`:
```python
employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
date_debut = models.DateField()
date_fin = models.DateField()
type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)
motif = models.TextField(blank=True)
statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
date_soumission = models.DateTimeField(auto_now_add=True)
```
Choices used by `DemandeConge`:
- `type_conge`: `annuel`, `maladie`, `autre`.
- `statut`: `en_attente`, `validee`, `refusee`.
## forms.py
`conges/forms.py` defines a `ModelForm`:
```python
class DemandeCongeForm(forms.ModelForm):
    class Meta:
        model = DemandeConge
        fields = ['date_debut', 'date_fin', 'type_conge', 'motif']
```
The employee can choose dates, type, and reason. The status is controlled by the app/responsible user.
## templates/
Templates are HTML files. They use inheritance:
```django
{% extends 'conges/base.html' %}
{% block content %}{% endblock %}
```
They display variables like `{{ employe.solde_conges }}`, loops like `{% for demande in demandes %}`, and conditions like `{% if demande.statut == 'validee' %}`.
## static/
Static files are CSS, JS, images. This project uses `conges/static/conges/styles.css`, loaded in `base.html` with `{% static 'conges/styles.css' %}`.
## admin.py
`conges/admin.py` registers models:
```python
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
```
```python
@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
```
Simple style would be `admin.site.register(ModelName)`: `admin` is the module, `site` is the admin site object, and `register()` adds the model to admin.
## migrations/
Migrations are auto-generated database change files. `conges/migrations/0001_initial.py` creates the `Employe` and `DemandeConge` tables. `makemigrations` creates migrations; `migrate` applies them.

# 8. What was manually written vs generated by Django
| Part | Generated by Django? | Usually written manually? | Explanation |
|---|---|---|---|
| `manage.py` | Yes | No | Created when project starts |
| `config/settings.py` | Mostly yes | Sometimes edited | Apps, database, login URL |
| `config/urls.py` | Mostly yes | Edited | Includes `conges.urls` and admin |
| `config/asgi.py`, `config/wsgi.py` | Yes | Rarely | Deployment entry files |
| `conges/apps.py` | Yes | Rarely | App configuration |
| `conges/models.py` | Empty file generated | Yes | Database tables |
| `conges/views.py` | Empty file generated | Yes | Page logic |
| `conges/urls.py` | No | Yes | App routes |
| `conges/forms.py` | No | Yes | Leave form |
| `conges/admin.py` | Empty file generated | Yes | Admin configuration |
| `conges/templates/` | No | Yes | HTML pages |
| `conges/static/` | No | Yes | CSS |
| `conges/migrations/` | Yes | No | Auto-created DB changes |
| `db.sqlite3` | Created by commands | No | Local database |
| `init_data.py` | No | Yes | Demo users |
| `myapp/` | Yes | No active code | Not installed in settings |

# 9. Main features of the HR holiday request app
## Login/logout
Files: `conges/views.py`, `conges/templates/conges/login.html`, `conges/urls.py`.
Login uses `AuthenticationForm`, `authenticate()`, `login()`, and messages. Logout uses `logout()` and redirects to login.
## Employee dashboard
Files: `employe_home` view, `employe_home.html`, `Employe`, `DemandeConge`.
The employee sees leave balance, total requests, pending requests, recent history, and a link to create a new request.
## Submit leave request
Files: `soumettre_demande`, `DemandeCongeForm`, `soumettre_demande.html`, `DemandeConge`.
Steps:
1. Employee opens `/soumettre/`.
2. Django displays the form.
3. Employee submits POST data.
4. Form is validated.
5. Request is saved with status `en_attente`.
6. Employee is redirected to the dashboard.
## Request history
Files: `historique_demandes`, `historique_demandes.html`, `conges/tests.py`.
Employees see only their own requests. Staff/superusers see all requests.
## Responsible dashboard
Files: `responsable_home`, `responsable_home.html`, `DemandeConge`.
Staff users see pending requests and counters. Non-staff users are redirected to the employee page.
## Approve/refuse request
Files: `traiter_demande`, buttons in `responsable_home.html`, `DemandeConge`.
The responsible user clicks `Valider` or `Refuser`. The view changes `statut` to `validee` or `refusee`.
## Admin panel
Files: `config/urls.py`, `conges/admin.py`. Admin can view and manage users, employees, and leave requests.

# 10. Database explanation
This project uses SQLite in `db.sqlite3`. SQLite is a simple file-based database, good for demos and small projects.
Analogy: a model is like an Excel table structure; each saved object is one row.
Main tables/models:
| Table/model | Purpose |
|---|---|
| `auth_user` | Django users |
| `conges_employe` / `Employe` | Employee leave profile |
| `conges_demandeconge` / `DemandeConge` | Leave requests |
| `django_session` | Login sessions |
| `django_migrations` | Migration history |
Relationships:
```text
User -> one-to-one -> Employe -> one-to-many -> DemandeConge
```
`OneToOneField` means one user has one employee profile. `ForeignKey` means one employee can have many leave requests. `on_delete=models.CASCADE` means related records are deleted when the parent is deleted.

# 11. Authentication and users
The project uses Django's built-in authentication. Users are stored in Django's `User` model.
Login is handled by `AuthenticationForm`, `authenticate()`, `login()`, and `logout()`.
Roles:
| Role | Django flag | Behavior |
|---|---|---|
| Employee | `is_staff=False` | Own dashboard and own requests |
| Responsible/HR | `is_staff=True` | Can process pending requests |
| Admin | `is_superuser=True` | Can use full admin panel |
Access control uses:
```python
@login_required
```
Staff-only logic uses:
```python
if not request.user.is_staff:
    return redirect('conges:employe_home')
```
There is no custom registration page. Users are created with `init_data.py`, Django admin, or `python manage.py createsuperuser`.

# 12. Forms and validation
A form collects and validates user input. This project uses `DemandeCongeForm` in `conges/forms.py`.
Fields shown to the employee:
- `date_debut`
- `date_fin`
- `type_conge`
- `motif`
GET vs POST:
| Method | Meaning | Project example |
|---|---|---|
| GET | Open/read a page | Open `/soumettre/` |
| POST | Send data/action | Submit leave request |
`request.method` tells the view which method was used. `form.is_valid()` checks the data before saving.
Concrete example:
```text
Employee fills form -> browser sends POST -> Django validates -> view assigns employee -> request is saved -> redirect
```
Important limit: validation is mostly Django field validation. There is no custom rule checking `date_fin >= date_debut`.

# 13. Templates and frontend
Templates build the HTML pages. Main template: `conges/templates/conges/base.html`.
`base.html` contains Bootstrap CDN, local CSS, sidebar, top bar, logout button, message display, and `{% block content %}`.
Other templates:
| Template | Purpose |
|---|---|
| `login.html` | Login form and demo credentials |
| `employe_home.html` | Employee dashboard |
| `responsable_home.html` | Responsible dashboard |
| `soumettre_demande.html` | Leave request form |
| `historique_demandes.html` | Request history |
Bootstrap is loaded in `base.html` from CDN. Custom CSS is `conges/static/conges/styles.css`.
The CSS creates the dashboard layout, sidebar, cards, tables, badges, buttons, and responsive behavior.
Backend vs frontend: backend is Python/Django logic and database; frontend is HTML/CSS shown in the browser.

# 14. Admin panel explanation
Django admin is a built-in management interface at `http://127.0.0.1:8000/admin/`.
Why it is useful:
- It proves data is saved.
- It lets the admin inspect users, employees, and requests.
- It provides filters/search with little code.
Models visible through this app: `Employe` and `DemandeConge`.
Real admin code:
```python
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('user', 'solde_conges')
```
```python
@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_debut', 'date_fin', 'type_conge', 'statut', 'date_soumission')
    list_filter = ('statut', 'type_conge')
    search_fields = ('employe__user__username', 'motif')
```
`ModelAdmin` customizes display. `list_display` chooses columns. `list_filter` adds filters. `search_fields` adds search.

# 15. Common code snippets explained
Imports:
```python
from django.shortcuts import get_object_or_404, redirect, render
from .models import DemandeConge, Employe
from .forms import DemandeCongeForm
```
`render` returns HTML, `redirect` sends the browser elsewhere, `get_object_or_404` safely finds an object or returns 404. `.models` and `.forms` mean "from this app".
View function:
```python
def login_view(request):
```
`request` contains browser request information. Django calls this function for the matching URL.
POST check:
```python
if request.method == 'POST':
```
This means the user submitted a form.
Form validation and save:
```python
form = DemandeCongeForm(request.POST or None)
if form.is_valid():
    demande = form.save(commit=False)
    demande.employe = employe
    demande.save()
```
Line by line: create form, validate data, create object without saving, attach logged-in employee, save to database.
Queries:
```python
DemandeConge.objects.filter(employe=employe)
DemandeConge.objects.filter(statut='en_attente')
DemandeConge.objects.count()
```
These get personal requests, pending requests, and request counts.
Safe lookup:
```python
demande = get_object_or_404(DemandeConge, id=demande_id)
```
This avoids crashing if the request ID does not exist.
Login protection:
```python
@login_required
```
This means the page requires a logged-in user.
CSRF token:
```django
{% csrf_token %}
```
This protects POST forms from fake external submissions.
Template loop:
```django
{% for demande in demandes %}
    {{ demande.date_debut }}
{% empty %}
    Aucune demande pour le moment.
{% endfor %}
```
This displays rows or an empty message.

# 16. Technical questions the jury may ask
| Question | Simple answer |
|---|---|
| 1. What is Django? | A Python framework for building web apps quickly. |
| 2. Why Django? | It provides routing, ORM, forms, login, admin, and security basics. |
| 3. What is MVT? | Model, View, Template: data, logic, display. |
| 4. Model vs view vs template? | Model stores data, view handles logic, template shows HTML. |
| 5. What is `manage.py`? | The command center for server, migrations, users, and tests. |
| 6. What is `settings.py`? | Configuration for apps, database, templates, static files. |
| 7. What is `urls.py`? | It maps URLs to views. |
| 8. What does `render()` do? | Combines a template with data and returns HTML. |
| 9. What is a model? | A Python class representing a database table. |
| 10. What is a migration? | A file describing database changes. |
| 11. Why run migrations? | To create/update database tables from models. |
| 12. What is SQLite? | A simple database stored in one file. |
| 13. What is a Django form? | A class that displays and validates input. |
| 14. What are GET and POST? | GET reads pages; POST sends data/actions. |
| 15. What does `form.is_valid()` do? | Checks submitted data before saving. |
| 16. What is CSRF token? | A security token protecting forms. |
| 17. What is `admin.site.register()`? | It adds a model to admin; this project uses `@admin.register`. |
| 18. How is a holiday request saved? | The form is validated, linked to the employee, then saved as `DemandeConge`. |
| 19. How does HR approve/refuse? | Staff submits a POST action; `traiter_demande` updates `statut`. |
| 20. What are the limits? | Simple roles, no automatic balance reduction, no emails, no production deployment. |
| 21. Future improvements? | Better permissions, balance calculation, email, PDF, PostgreSQL, audit history. |

# 17. Demo script for tomorrow
1. Start the server: `python manage.py runserver`. Say: "I am starting the local Django development server."
2. Open `http://127.0.0.1:8000/`. Say: "The app redirects users based on login and role."
3. Login as employee: `employe1 / employe123`. Show balance, history, and new request button. Say: "An employee can submit and follow personal requests."
4. Submit a request. Say: "The browser sends POST data, Django validates it, and saves a `DemandeConge`."
5. Open `/historique/`. Say: "A normal employee only sees their own requests."
6. Login as responsible: `responsable1 / responsable123`. Show pending requests. Say: "A responsible user is represented by `is_staff=True`."
7. Click `Valider` or `Refuser`. Say: "This updates the request status in the database."
8. Open `/admin/` and login with `admin / admin123`. Say: "Django admin lets administrators inspect and manage saved data."
Avoid saying:
- "This is production ready."
- "Leave balance is automatically reduced."
- "Users can register themselves."
- "The app sends email notifications."
Better phrase: "This is a functional demo with clear future improvements."

# 18. Simple oral explanation of the project
This project is a Django web application for managing employee holiday requests. An employee can log in, see their leave balance, view their request history, and submit a new leave request with dates, type, and reason. A responsible user can log in and see pending requests, then approve or refuse them. The application uses Django models to store employees and leave requests in SQLite, views to control the logic, templates to display pages, and Django authentication and admin to manage users and data.

# 19. Limits and possible improvements
Current limits:
- Leave balance is displayed but not automatically reduced after approval.
- Role logic is simple: `is_staff` means responsible/admin access.
- There is no custom registration page.
- There is no email notification.
- There is no PDF export.
- There is no deployment setup.
- There is no audit history.
- SQLite is good for demos but not ideal for a big company.
- There is no custom validation that checks `date_fin >= date_debut`.
- `myapp` exists but appears unused.
Possible improvements:
| Improvement | Why it helps |
|---|---|
| Better role permissions | Separate employee, HR, manager, admin |
| Leave balance calculation | Reduce balance after approved leave |
| Date validation | Prevent impossible date ranges |
| Email notifications | Inform users about decisions |
| Better UI | Improve presentation and usability |
| PDF export | Export reports |
| PostgreSQL | Better production database |
| Deployment | Make it accessible online |
| Audit history | Track who approved/refused and when |
| More tests | Protect important workflows |
Positive explanation: "The current project implements the main workflow. These points are future improvements for a production version."

# 20. Final quick revision sheet
## 10 key words
| Word | Meaning |
|---|---|
| Django | Python web framework |
| Model | Database table structure |
| View | Python logic |
| Template | HTML page |
| URL | Route to a view |
| Form | Collects and validates input |
| ORM | Python way to query the database |
| Migration | Database change file |
| SQLite | File-based database |
| CSRF | Form security protection |
## 10 commands
| Command | Role |
|---|---|
| `python -m venv venv` | Create virtual environment |
| `venv\Scripts\activate` | Activate on Windows |
| `source venv/bin/activate` | Activate on Linux/Mac |
| `pip install Django==6.0.4` | Install Django |
| `python manage.py migrate` | Apply migrations |
| `python init_data.py` | Create demo users |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py runserver` | Start server |
| `python manage.py check` | Check project |
| `python manage.py test conges` | Run tests |
## 10 files and their roles
| File | Role |
|---|---|
| `manage.py` | Command center |
| `config/settings.py` | Project settings |
| `config/urls.py` | Main routes |
| `conges/urls.py` | App routes |
| `conges/views.py` | Logic |
| `conges/models.py` | Data models |
| `conges/forms.py` | Leave form |
| `conges/admin.py` | Admin setup |
| `conges/templates/conges/base.html` | Shared layout |
| `conges/static/conges/styles.css` | Styling |
## 10 jury questions with one-line answers
| Question | One-line answer |
|---|---|
| What does the app do? | It manages employee leave requests. |
| Who uses it? | Employees, responsible/HR users, and admins. |
| What is Django? | A Python framework for web apps. |
| What is MVT? | Model for data, view for logic, template for display. |
| Where are URLs defined? | `config/urls.py` and `conges/urls.py`. |
| Where is logic written? | `conges/views.py`. |
| Where is data structure defined? | `conges/models.py`. |
| How is a request saved? | Through `DemandeCongeForm` and `DemandeConge.save()`. |
| How does HR approve/refuse? | A staff POST action updates `statut`. |
| Main improvement? | Automatic leave balance and stronger permissions. |
Final memory sentence: "My project is a Django HR leave request app. Employees submit requests, staff users approve or refuse them, and Django handles routing, views, templates, models, forms, authentication, and admin."
# 1. Project overview
This project is a Django web application for managing employee holiday/leave requests.
- Employees log in, view their leave balance/history, and submit requests.
- Responsible/HR users log in, view pending requests, and approve or refuse them.
- Admin users can manage data through Django Admin at `/admin/`.
Main goal: replace a manual leave request process with a small web system.
Real-life scenario: an employee wants holiday leave, fills a request form, and HR/admin checks it and approves or refuses it.
The active app is `conges` ("leave" in French). The project is a good demo because it shows login, roles, forms, database records, templates, admin, and a complete approval workflow.
Important: this is a demo/local application, not a full production HR platform yet.

# 2. Why Django was used
Django is a Python web framework. A framework is a ready-made toolbox for building web applications faster.
Real-life analogy: Django is like a ready-made building structure. The walls, doors, electricity, and water are already prepared; the developer customizes the rooms.
Why Django fits this project:
| Django feature | How this project uses it |
|---|---|
| Routing/URLs | Maps `/login/`, `/soumettre/`, `/admin/` to code |
| Views | Runs page logic in `conges/views.py` |
| Templates | Shows HTML pages from `conges/templates/conges/` |
| Models/ORM | Stores employees and leave requests |
| Forms | Validates leave request input |
| Admin panel | Gives management UI at `/admin/` |
| Authentication | Uses Django users, login, logout, staff/admin flags |
| CSRF security | Protects POST forms with `{% csrf_token %}` |
Django is faster than scratch because password handling, sessions, database queries, form security, and admin pages already exist.
This project uses Django's built-in `User` model for usernames, passwords, staff status, and superuser status.

# 3. Django architecture explained simply
Django uses MVT: Model, View, Template.
| Part | Simple meaning | Real file example |
|---|---|---|
| Model | Data/database structure | `conges/models.py` |
| View | Logic/controller | `conges/views.py` |
| Template | Visual HTML page | `conges/templates/conges/*.html` |
MVT compared with MVC:
- Model = data.
- Django View = controller/logic.
- Template = visual page.
Real-life analogy:
| Django part | Analogy |
|---|---|
| URL | Road/signpost |
| View | Receptionist/worker who decides what to do |
| Model | Filing cabinet structure |
| Database | Archive/storage room |
| Template | Printed page shown to the user |
Flow:
```text
Browser URL -> urls.py -> view -> model/database if needed -> template -> HTML response
```
Example: `/soumettre/` goes to `soumettre_demande`, which prepares/saves a `DemandeConge` and shows `soumettre_demande.html`.

# 4. Full project structure
Real project tree:
```text
demo_d/
|-- manage.py
|-- db.sqlite3
|-- init_data.py
|-- GUIDE.md
|-- PROJECT_EXPLANATION_GUIDE.md
|-- config/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- conges/
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/0001_initial.py
|   |-- static/conges/styles.css
|   `-- templates/conges/
|       |-- base.html
|       |-- login.html
|       |-- employe_home.html
|       |-- responsable_home.html
|       |-- soumettre_demande.html
|       `-- historique_demandes.html
`-- myapp/
    |-- admin.py
    |-- apps.py
    |-- models.py
    |-- tests.py
    |-- views.py
    `-- migrations/__init__.py
```
Important files:
| File/folder | Used for | Generated or manual? | Why it matters |
|---|---|---|---|
| `manage.py` | Commands | Generated | Runs server, migrations, tests |
| `config/` | Project folder | Generated | Global Django configuration |
| `config/settings.py` | Settings | Generated then edited | Apps, database, templates, static files |
| `config/urls.py` | Main URLs | Generated then edited | Includes `conges.urls` and admin |
| `conges/` | Main app | Generated then developed | Contains HR leave logic |
| `conges/models.py` | Models | Manual code | Defines `Employe`, `DemandeConge` |
| `conges/views.py` | Logic | Manual code | Login, dashboards, submit, approve/refuse |
| `conges/forms.py` | Forms | Manual | Defines `DemandeCongeForm` |
| `conges/admin.py` | Admin setup | Manual code | Shows models in admin |
| `conges/templates/` | HTML pages | Manual | User interface |
| `conges/static/conges/styles.css` | CSS | Manual | Layout, cards, tables, badges |
| `conges/migrations/0001_initial.py` | DB creation | Auto-generated | Creates app tables |
| `conges/tests.py` | Tests | Manual | Tests history visibility |
| `db.sqlite3` | Database | Created by Django | Stores users, employees, requests |
| `init_data.py` | Demo data | Manual | Creates test users |
| `myapp/` | Mostly unused app | Generated | Not in `INSTALLED_APPS` |
The Django project folder is `config`. The active Django app is `conges`. `myapp` exists but is not active in `config/settings.py`.

# 5. How to run the project
There is no `requirements.txt`.
Detected local environment: Python `3.14.3`, Django `6.0.4`.
Windows commands:
```bat
python -m venv venv
venv\Scripts\activate
pip install Django==6.0.4
python manage.py migrate
python init_data.py
python manage.py createsuperuser
python manage.py runserver
```
Linux/Mac commands:
```bash
python3 -m venv venv
source venv/bin/activate
pip install Django==6.0.4
python manage.py migrate
python init_data.py
python manage.py createsuperuser
python manage.py runserver
```
If using the existing `.venv`:
```bash
.venv/bin/python manage.py migrate
.venv/bin/python init_data.py
.venv/bin/python manage.py runserver
```
Open the app: `http://127.0.0.1:8000/`.
Open admin: `http://127.0.0.1:8000/admin/`.
Demo accounts from `init_data.py` and `login.html`:
| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `admin123` |
| Employee | `employe1` | `employe123` |
| Responsible/HR | `responsable1` | `responsable123` |
`python init_data.py` is optional, but useful because it creates these demo accounts.

# 6. Request flow: what happens when a user opens a page
General Django flow:
1. User enters a URL in the browser.
2. Django checks `config/urls.py`.
3. `config/urls.py` includes `conges/urls.py`.
4. `conges/urls.py` calls a view in `conges/views.py`.
5. The view reads/writes models if needed.
6. The view returns HTML with `render()` or redirects with `redirect()`.
7. The browser displays the page.
Real example: submitting leave.
```text
/soumettre/ -> conges/urls.py -> soumettre_demande -> DemandeCongeForm -> DemandeConge -> soumettre_demande.html
```
Actual route:
```python
path('soumettre/', views.soumettre_demande, name='soumettre_demande')
```
Important code:
```python
form = DemandeCongeForm(request.POST or None)
if request.method == 'POST' and form.is_valid():
    demande = form.save(commit=False)
    demande.employe = employe
    demande.save()
    return redirect('conges:employe_home')
```
Meaning: validate the submitted form, create a request, attach the current employee, save it, and return to the employee dashboard.

# 7. Important Django concepts used in this project
## manage.py
`manage.py` is the command center. It runs commands like:
```bash
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py test conges
```
It points Django to `config.settings`. Analogy: it is the remote control for the project.
## settings.py
`config/settings.py` contains configuration. Important real parts:
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
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
LOGIN_URL = 'conges:login'
```
This activates `conges`, uses SQLite, and sends unauthenticated users to login.
## urls.py
`urls.py` is the GPS map from browser address to view. `config/urls.py` includes:
```python
path('', include('conges.urls'))
path('admin/', admin.site.urls)
```
Real routes:
| URL | View |
|---|---|
| `/` | `dashboard_view` |
| `/login/` | `login_view` |
| `/logout/` | `logout_view` |
| `/employe/` | `employe_home` |
| `/historique/` | `historique_demandes` |
| `/soumettre/` | `soumettre_demande` |
| `/responsable/` | `responsable_home` |
| `/traiter/<int:demande_id>/` | `traiter_demande` |
| `/admin/` | Django admin |
## views.py
`conges/views.py` contains function-based views. A view receives `request` and returns a response.
```python
@login_required
def employe_home(request):
    employe, created = Employe.objects.get_or_create(user=request.user)
    demandes = DemandeConge.objects.filter(employe=employe)
```
This creates/fetches the employee profile and lists only that employee's requests.
## render()
`render()` combines request, template, and data:
```python
return render(request, 'conges/login.html', {'form': form})
```
## redirect()
`redirect()` sends the user to another page:
```python
return redirect('conges:dashboard')
```
## models.py
`conges/models.py` defines database tables. `Employe`:
```python
user = models.OneToOneField(User, on_delete=models.CASCADE)
solde_conges = models.IntegerField(default=25)
```
`DemandeConge`:
```python
employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
date_debut = models.DateField()
date_fin = models.DateField()
type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)
motif = models.TextField(blank=True)
statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
date_soumission = models.DateTimeField(auto_now_add=True)
```
Choices used by `DemandeConge`:
- `type_conge`: `annuel`, `maladie`, `autre`.
- `statut`: `en_attente`, `validee`, `refusee`.
## forms.py
`conges/forms.py` defines a `ModelForm`:
```python
class DemandeCongeForm(forms.ModelForm):
    class Meta:
        model = DemandeConge
        fields = ['date_debut', 'date_fin', 'type_conge', 'motif']
```
The employee can choose dates, type, and reason. The status is controlled by the app/responsible user.
## templates/
Templates are HTML files. They use inheritance:
```django
{% extends 'conges/base.html' %}
{% block content %}{% endblock %}
```
They display variables like `{{ employe.solde_conges }}`, loops like `{% for demande in demandes %}`, and conditions like `{% if demande.statut == 'validee' %}`.
## static/
Static files are CSS, JS, images. This project uses `conges/static/conges/styles.css`, loaded in `base.html` with `{% static 'conges/styles.css' %}`.
## admin.py
`conges/admin.py` registers models:
```python
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
```
```python
@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
```
Simple style would be `admin.site.register(ModelName)`: `admin` is the module, `site` is the admin site object, and `register()` adds the model to admin.
## migrations/
Migrations are auto-generated database change files. `conges/migrations/0001_initial.py` creates the `Employe` and `DemandeConge` tables. `makemigrations` creates migrations; `migrate` applies them.

# 8. What was manually written vs generated by Django
| Part | Generated by Django? | Usually written manually? | Explanation |
|---|---|---|---|
| `manage.py` | Yes | No | Created when project starts |
| `config/settings.py` | Mostly yes | Sometimes edited | Apps, database, login URL |
| `config/urls.py` | Mostly yes | Edited | Includes `conges.urls` and admin |
| `config/asgi.py`, `config/wsgi.py` | Yes | Rarely | Deployment entry files |
| `conges/apps.py` | Yes | Rarely | App configuration |
| `conges/models.py` | Empty file generated | Yes | Database tables |
| `conges/views.py` | Empty file generated | Yes | Page logic |
| `conges/urls.py` | No | Yes | App routes |
| `conges/forms.py` | No | Yes | Leave form |
| `conges/admin.py` | Empty file generated | Yes | Admin configuration |
| `conges/templates/` | No | Yes | HTML pages |
| `conges/static/` | No | Yes | CSS |
| `conges/migrations/` | Yes | No | Auto-created DB changes |
| `db.sqlite3` | Created by commands | No | Local database |
| `init_data.py` | No | Yes | Demo users |
| `myapp/` | Yes | No active code | Not installed in settings |

# 9. Main features of the HR holiday request app
## Login/logout
Files: `conges/views.py`, `conges/templates/conges/login.html`, `conges/urls.py`.
Login uses `AuthenticationForm`, `authenticate()`, `login()`, and messages. Logout uses `logout()` and redirects to login.
## Employee dashboard
Files: `employe_home` view, `employe_home.html`, `Employe`, `DemandeConge`.
The employee sees leave balance, total requests, pending requests, recent history, and a link to create a new request.
## Submit leave request
Files: `soumettre_demande`, `DemandeCongeForm`, `soumettre_demande.html`, `DemandeConge`.
Steps:
1. Employee opens `/soumettre/`.
2. Django displays the form.
3. Employee submits POST data.
4. Form is validated.
5. Request is saved with status `en_attente`.
6. Employee is redirected to the dashboard.
## Request history
Files: `historique_demandes`, `historique_demandes.html`, `conges/tests.py`.
Employees see only their own requests. Staff/superusers see all requests.
## Responsible dashboard
Files: `responsable_home`, `responsable_home.html`, `DemandeConge`.
Staff users see pending requests and counters. Non-staff users are redirected to the employee page.
## Approve/refuse request
Files: `traiter_demande`, buttons in `responsable_home.html`, `DemandeConge`.
The responsible user clicks `Valider` or `Refuser`. The view changes `statut` to `validee` or `refusee`.
## Admin panel
Files: `config/urls.py`, `conges/admin.py`. Admin can view and manage users, employees, and leave requests.

# 10. Database explanation
This project uses SQLite in `db.sqlite3`. SQLite is a simple file-based database, good for demos and small projects.
Analogy: a model is like an Excel table structure; each saved object is one row.
Main tables/models:
| Table/model | Purpose |
|---|---|
| `auth_user` | Django users |
| `conges_employe` / `Employe` | Employee leave profile |
| `conges_demandeconge` / `DemandeConge` | Leave requests |
| `django_session` | Login sessions |
| `django_migrations` | Migration history |
Relationships:
```text
User -> one-to-one -> Employe -> one-to-many -> DemandeConge
```
`OneToOneField` means one user has one employee profile. `ForeignKey` means one employee can have many leave requests. `on_delete=models.CASCADE` means related records are deleted when the parent is deleted.

# 11. Authentication and users
The project uses Django's built-in authentication. Users are stored in Django's `User` model.
Login is handled by `AuthenticationForm`, `authenticate()`, `login()`, and `logout()`.
Roles:
| Role | Django flag | Behavior |
|---|---|---|
| Employee | `is_staff=False` | Own dashboard and own requests |
| Responsible/HR | `is_staff=True` | Can process pending requests |
| Admin | `is_superuser=True` | Can use full admin panel |
Access control uses:
```python
@login_required
```
Staff-only logic uses:
```python
if not request.user.is_staff:
    return redirect('conges:employe_home')
```
There is no custom registration page. Users are created with `init_data.py`, Django admin, or `python manage.py createsuperuser`.

# 12. Forms and validation
A form collects and validates user input. This project uses `DemandeCongeForm` in `conges/forms.py`.
Fields shown to the employee:
- `date_debut`
- `date_fin`
- `type_conge`
- `motif`
GET vs POST:
| Method | Meaning | Project example |
|---|---|---|
| GET | Open/read a page | Open `/soumettre/` |
| POST | Send data/action | Submit leave request |
`request.method` tells the view which method was used. `form.is_valid()` checks the data before saving.
Concrete example:
```text
Employee fills form -> browser sends POST -> Django validates -> view assigns employee -> request is saved -> redirect
```
Important limit: validation is mostly Django field validation. There is no custom rule checking `date_fin >= date_debut`.

# 13. Templates and frontend
Templates build the HTML pages. Main template: `conges/templates/conges/base.html`.
`base.html` contains Bootstrap CDN, local CSS, sidebar, top bar, logout button, message display, and `{% block content %}`.
Other templates:
| Template | Purpose |
|---|---|
| `login.html` | Login form and demo credentials |
| `employe_home.html` | Employee dashboard |
| `responsable_home.html` | Responsible dashboard |
| `soumettre_demande.html` | Leave request form |
| `historique_demandes.html` | Request history |
Bootstrap is loaded in `base.html` from CDN. Custom CSS is `conges/static/conges/styles.css`.
The CSS creates the dashboard layout, sidebar, cards, tables, badges, buttons, and responsive behavior.
Backend vs frontend: backend is Python/Django logic and database; frontend is HTML/CSS shown in the browser.

# 14. Admin panel explanation
Django admin is a built-in management interface at `http://127.0.0.1:8000/admin/`.
Why it is useful:
- It proves data is saved.
- It lets the admin inspect users, employees, and requests.
- It provides filters/search with little code.
Models visible through this app: `Employe` and `DemandeConge`.
Real admin code:
```python
@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('user', 'solde_conges')
```
```python
@admin.register(DemandeConge)
class DemandeCongeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'date_debut', 'date_fin', 'type_conge', 'statut', 'date_soumission')
    list_filter = ('statut', 'type_conge')
    search_fields = ('employe__user__username', 'motif')
```
`ModelAdmin` customizes display. `list_display` chooses columns. `list_filter` adds filters. `search_fields` adds search.

# 15. Common code snippets explained
Imports:
```python
from django.shortcuts import get_object_or_404, redirect, render
from .models import DemandeConge, Employe
from .forms import DemandeCongeForm
```
`render` returns HTML, `redirect` sends the browser elsewhere, `get_object_or_404` safely finds an object or returns 404. `.models` and `.forms` mean "from this app".
View function:
```python
def login_view(request):
```
`request` contains browser request information. Django calls this function for the matching URL.
POST check:
```python
if request.method == 'POST':
```
This means the user submitted a form.
Form validation and save:
```python
form = DemandeCongeForm(request.POST or None)
if form.is_valid():
    demande = form.save(commit=False)
    demande.employe = employe
    demande.save()
```
Line by line: create form, validate data, create object without saving, attach logged-in employee, save to database.
Queries:
```python
DemandeConge.objects.filter(employe=employe)
DemandeConge.objects.filter(statut='en_attente')
DemandeConge.objects.count()
```
These get personal requests, pending requests, and request counts.
Safe lookup:
```python
demande = get_object_or_404(DemandeConge, id=demande_id)
```
This avoids crashing if the request ID does not exist.
Login protection:
```python
@login_required
```
This means the page requires a logged-in user.
CSRF token:
```django
{% csrf_token %}
```
This protects POST forms from fake external submissions.
Template loop:
```django
{% for demande in demandes %}
    {{ demande.date_debut }}
{% empty %}
    Aucune demande pour le moment.
{% endfor %}
```
This displays rows or an empty message.

# 16. Technical questions the jury may ask
| Question | Simple answer |
|---|---|
| 1. What is Django? | A Python framework for building web apps quickly. |
| 2. Why Django? | It provides routing, ORM, forms, login, admin, and security basics. |
| 3. What is MVT? | Model, View, Template: data, logic, display. |
| 4. Model vs view vs template? | Model stores data, view handles logic, template shows HTML. |
| 5. What is `manage.py`? | The command center for server, migrations, users, and tests. |
| 6. What is `settings.py`? | Configuration for apps, database, templates, static files. |
| 7. What is `urls.py`? | It maps URLs to views. |
| 8. What does `render()` do? | Combines a template with data and returns HTML. |
| 9. What is a model? | A Python class representing a database table. |
| 10. What is a migration? | A file describing database changes. |
| 11. Why run migrations? | To create/update database tables from models. |
| 12. What is SQLite? | A simple database stored in one file. |
| 13. What is a Django form? | A class that displays and validates input. |
| 14. What are GET and POST? | GET reads pages; POST sends data/actions. |
| 15. What does `form.is_valid()` do? | Checks submitted data before saving. |
| 16. What is CSRF token? | A security token protecting forms. |
| 17. What is `admin.site.register()`? | It adds a model to admin; this project uses `@admin.register`. |
| 18. How is a holiday request saved? | The form is validated, linked to the employee, then saved as `DemandeConge`. |
| 19. How does HR approve/refuse? | Staff submits a POST action; `traiter_demande` updates `statut`. |
| 20. What are the limits? | Simple roles, no automatic balance reduction, no emails, no production deployment. |
| 21. Future improvements? | Better permissions, balance calculation, email, PDF, PostgreSQL, audit history. |

# 17. Demo script for tomorrow
1. Start the server: `python manage.py runserver`. Say: "I am starting the local Django development server."
2. Open `http://127.0.0.1:8000/`. Say: "The app redirects users based on login and role."
3. Login as employee: `employe1 / employe123`. Show balance, history, and new request button. Say: "An employee can submit and follow personal requests."
4. Submit a request. Say: "The browser sends POST data, Django validates it, and saves a `DemandeConge`."
5. Open `/historique/`. Say: "A normal employee only sees their own requests."
6. Login as responsible: `responsable1 / responsable123`. Show pending requests. Say: "A responsible user is represented by `is_staff=True`."
7. Click `Valider` or `Refuser`. Say: "This updates the request status in the database."
8. Open `/admin/` and login with `admin / admin123`. Say: "Django admin lets administrators inspect and manage saved data."
Avoid saying:
- "This is production ready."
- "Leave balance is automatically reduced."
- "Users can register themselves."
- "The app sends email notifications."
Better phrase: "This is a functional demo with clear future improvements."

# 18. Simple oral explanation of the project
This project is a Django web application for managing employee holiday requests. An employee can log in, see their leave balance, view their request history, and submit a new leave request with dates, type, and reason. A responsible user can log in and see pending requests, then approve or refuse them. The application uses Django models to store employees and leave requests in SQLite, views to control the logic, templates to display pages, and Django authentication and admin to manage users and data.

# 19. Limits and possible improvements
Current limits:
- Leave balance is displayed but not automatically reduced after approval.
- Role logic is simple: `is_staff` means responsible/admin access.
- There is no custom registration page.
- There is no email notification.
- There is no PDF export.
- There is no deployment setup.
- There is no audit history.
- SQLite is good for demos but not ideal for a big company.
- There is no custom validation that checks `date_fin >= date_debut`.
- `myapp` exists but appears unused.
Possible improvements:
| Improvement | Why it helps |
|---|---|
| Better role permissions | Separate employee, HR, manager, admin |
| Leave balance calculation | Reduce balance after approved leave |
| Date validation | Prevent impossible date ranges |
| Email notifications | Inform users about decisions |
| Better UI | Improve presentation and usability |
| PDF export | Export reports |
| PostgreSQL | Better production database |
| Deployment | Make it accessible online |
| Audit history | Track who approved/refused and when |
| More tests | Protect important workflows |
Positive explanation: "The current project implements the main workflow. These points are future improvements for a production version."

# 20. Final quick revision sheet
## 10 key words
| Word | Meaning |
|---|---|
| Django | Python web framework |
| Model | Database table structure |
| View | Python logic |
| Template | HTML page |
| URL | Route to a view |
| Form | Collects and validates input |
| ORM | Python way to query the database |
| Migration | Database change file |
| SQLite | File-based database |
| CSRF | Form security protection |
## 10 commands
| Command | Role |
|---|---|
| `python -m venv venv` | Create virtual environment |
| `venv\Scripts\activate` | Activate on Windows |
| `source venv/bin/activate` | Activate on Linux/Mac |
| `pip install Django==6.0.4` | Install Django |
| `python manage.py migrate` | Apply migrations |
| `python init_data.py` | Create demo users |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py runserver` | Start server |
| `python manage.py check` | Check project |
| `python manage.py test conges` | Run tests |
## 10 files and their roles
| File | Role |
|---|---|
| `manage.py` | Command center |
| `config/settings.py` | Project settings |
| `config/urls.py` | Main routes |
| `conges/urls.py` | App routes |
| `conges/views.py` | Logic |
| `conges/models.py` | Data models |
| `conges/forms.py` | Leave form |
| `conges/admin.py` | Admin setup |
| `conges/templates/conges/base.html` | Shared layout |
| `conges/static/conges/styles.css` | Styling |
## 10 jury questions with one-line answers
| Question | One-line answer |
|---|---|
| What does the app do? | It manages employee leave requests. |
| Who uses it? | Employees, responsible/HR users, and admins. |
| What is Django? | A Python framework for web apps. |
| What is MVT? | Model for data, view for logic, template for display. |
| Where are URLs defined? | `config/urls.py` and `conges/urls.py`. |
| Where is logic written? | `conges/views.py`. |
| Where is data structure defined? | `conges/models.py`. |
| How is a request saved? | Through `DemandeCongeForm` and `DemandeConge.save()`. |
| How does HR approve/refuse? | A staff POST action updates `statut`. |
| Main improvement? | Automatic leave balance and stronger permissions. |
Final memory sentence: "My project is a Django HR leave request app. Employees submit requests, staff users approve or refuse them, and Django handles routing, views, templates, models, forms, authentication, and admin."
