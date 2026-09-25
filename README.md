# Full-Stack Web Development Course: HTML, CSS, JavaScript, Python and Django

Course material for a hands-on full-stack web development program. Learners progress from static pages to interactive front-end components, then to Python fundamentals, and finish by building and deploying a complete Django application.

Every module is made of short, focused exercises. Each exercise targets one concept and produces something visible in the browser or terminal.

## Learning path

| Stage | Module | Content |
| --- | --- | --- |
| 1 | HTML and CSS | 10 component exercises and two complete sample sites |
| 2 | JavaScript | DOM manipulation, events, form handling, 10 interactive components |
| 3 | Python | Syntax, control flow, object-oriented programming, file persistence |
| 4 | Django fundamentals | Project structure, models, migrations, admin |
| 5 | Capstone | Pharmacy management application, deployed to production |

## Repository structure

All material is under `PROGAMMATION WEB FORMATION/FORMATION PROGRAMMATION WEB/`:

```
application du html-css/
  site_exemple/                   Multi-page sample site
  site BTMS/                      Company landing page
applications django/
  exercices_html_css/             10 layout and component exercises
  exercices_html_css_js/          10 interactive component exercises
javascript/
  exercice, exercice_01..03/      Forms, DOM, counters
python/
  premierProgramme/               First Python program
  gestion_product/                Console product manager (OOP, modules)
  introduction-django/            First Django project (stock app)
  GestionPharmacie/               Capstone Django application
```

### HTML and CSS exercises

Simple page, profile card, call-to-action button, product card, navigation bar, footer, image gallery, contact form, timeline, pricing table.

### HTML, CSS and JavaScript exercises

Click counter, password visibility and strength, dark mode toggle, to-do list, quiz, modal dialog, tabs, image slider, form validation, accordion.

## Capstone: GestionPharmacie

A pharmacy management application built with Django, covering the complete lifecycle of a real project from data modelling to production deployment.

**Features**

- Product catalogue with categories, purchase and sale prices, batch numbers and expiry dates
- Stock tracking with low-stock alert thresholds
- Customer records (including allergies and ongoing treatments) and supplier directory
- Point of sale: sales with multiple line items, payment method and status, automatic stock decrement on validation
- Invoices, statistics, notifications and settings pages
- Authentication (login and logout)

**Production setup**

- Configuration through environment variables (`django-environ`)
- PostgreSQL in production, SQLite locally
- Static files served by WhiteNoise, application served by Gunicorn
- Deployed on Render; an administrator account is provisioned automatically on first deployment

The deployment walkthrough, written for learners, is in [`python/GestionPharmacie/DEPLOYMENT.md`](PROGAMMATION%20WEB%20FORMATION/FORMATION%20PROGRAMMATION%20WEB/python/GestionPharmacie/DEPLOYMENT.md).

### Run it locally

```bash
cd "PROGAMMATION WEB FORMATION/FORMATION PROGRAMMATION WEB/python/GestionPharmacie"
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then adjust the values
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Running the front-end exercises

Open the `index.html` file of any exercise directly in a browser. No build tools are required. The VS Code Live Server extension is convenient for automatic reload.

## Prerequisites

- A code editor (VS Code recommended)
- A modern browser
- Python 3.12 or later for the Python and Django modules
- Git

## Housekeeping

`python/introduction-django/env/` is a committed virtual environment. It is not needed to run the project and should be removed from version control and added to `.gitignore`.

## License

No license has been specified yet. Contact the author before reusing this material.
