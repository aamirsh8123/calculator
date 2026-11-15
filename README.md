# Code Studio — Material Code Calculator

A Django application for generating **Material Group** and **Product Hierarchy** codes from product specifications, including additive type, resin, ink type, color, and press.

## Features

- Guided calculator with dependent selections and automatically populated fields.
- Saved code lists and detailed specification views.
- Material definitions and color-code management for superusers.
- Django authentication and administration.
- Responsive interface with a workspace overview, styled forms, and tables.

## Technology

Python, Django 5.2.19 (LTS), Django REST Framework, django-crispy-forms, Bootstrap 4, jQuery, and SQLite. Python 3.12 is recommended; this project has been checked with Python 3.12.9.

## Setup on Windows (PowerShell)

```powershell
git clone https://github.com/aamirsh8123/calculator.git
cd calculator
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py create_groups
.\venv\Scripts\python.exe manage.py createsuperuser
New-Item -ItemType Directory -Path .\static -Force
.\venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser on the same computer. Keep the terminal open; press Ctrl+C to stop the server. Admin is available at http://127.0.0.1:8000/admin/.

### Initial reference data

A fresh database does not contain material definitions. Use Django admin to create item types, materials, and color codes before using the calculator. The existing calculator logic references specific item-type and material IDs; these records must match the expected mappings in `cal/forms.py`, `cal/views.py`, and the calculator JavaScript. No seed fixture is currently provided. Keep a separate backup of an existing configured database before migrating or replacing it.

Superusers manage materials and color codes. Authenticated users can calculate and browse codes. The `create_groups` command creates the existing Admin and User groups; material management views currently require superuser status.

## Project structure

| Path | Purpose |
| --- | --- |
| `manage.py` | Main management entry point; run commands from the repository root |
| `calculator/settings.py` | Active Django configuration |
| `calculator/urls.py` | Main URL configuration |
| `cal/` | Models, forms, views, serializers, and migrations |
| `cal/static/calculator/` | Calculator JavaScript and shared styling |
| `cal/templates/calculator/` | Application pages |
| `templates/` | Shared layout and authentication pages |
| `requirements.txt` | Pinned direct dependencies |

There is also a legacy nested configuration in `calculator/calculator/`. Use the root `manage.py` and the active configuration above.

## Checks

```powershell
.\venv\Scripts\python.exe -m pip check
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test
```

The regression suite covers authentication, access permissions, material forms, dependent selections, generated values, and saving/viewing codes. Tests use a separate test database. Bootstrap and jQuery are loaded from external CDNs and require browser internet access.

## Troubleshooting

**`No module named crispy_forms`:** use the virtual environment's Python for both installation and running Django, as shown above.

**Python library mismatch:** if another application sets `PYTHONHOME`, remove it for the current PowerShell session before running the commands:

```powershell
Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
```

**Missing static directory warning:** create the root `static` directory using the setup command above. Application assets live under `cal/static/`.

**Forgotten password:** reset it interactively:

```powershell
.\venv\Scripts\python.exe manage.py changepassword YOUR_USERNAME
```

## Deployment

The supplied settings are for local development. Before deployment, configure a private `SECRET_KEY`, disable `DEBUG`, set `ALLOWED_HOSTS`, configure static asset serving and HTTPS, and use a production WSGI/ASGI server. Do not use Django's development server for production. Review and update dependency versions before public deployment.

Virtual environments, Python caches, local databases, and environment files are excluded from new commits. Previously committed files remain in Git history; removing tracking does not erase history. Keep database backups separately.


## Dependency security

GitHub Actions checks dependencies, Django configuration, regression tests, and known dependency vulnerabilities on pushes, pull requests, and weekly. Dependabot checks Python dependencies and GitHub Actions weekly. Review and merge tested update pull requests to keep the application patched.
