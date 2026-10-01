# Universal Workforce Task Management System (Django)

Simple task management app built with plain HTML, CSS, Python, and Django only.

## Features
- Login page (custom template) + built-in Django admin panel for managing the admin user.
- Public registration always creates an Admin account. Workers are added by an Admin from the Workers page.
- Admin: dashboard with stats, add/remove workers, create & assign tasks (title, description, priority, deadline), view/filter/delete all tasks.
- Worker: view assigned tasks, move status Pending → In Progress → Completed, view completed tasks.
- Plain CSS only (core/static/core/style.css) — no frameworks, no JavaScript needed.

## Setup

1. Create a virtual environment and install Django:
   ```
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install django==5.0.7
   ```

2. Create the database:
   ```
   python manage.py migrate
   ```

3. Create your admin user (this is a Django superuser, used to log into both
   the app and /django-admin/):
   ```
   python manage.py createsuperuser
   ```
   Then open a shell and mark them as an app Admin (not just Django staff):
   ```
   python manage.py shell -c "from core.models import User; u=User.objects.get(username='YOUR_USERNAME'); u.role='ADMIN'; u.save()"
   ```
   (Anyone who registers through the app's /register/ page is automatically
   set to Admin, so this manual step is only needed for `createsuperuser`.)

4. Run the app:
   ```
   python manage.py runserver
   ```

5. Open http://localhost:8000
   - Login page: http://localhost:8000/login/
   - Register (new admin): http://localhost:8000/register/
   - Django's built-in admin panel: http://localhost:8000/django-admin/

## Project structure
- `workforce/` — Django project settings and root URLs
- `core/` — the app: models, views, forms, urls
- `core/templates/` — HTML templates (plain Django template language)
- `core/static/core/style.css` — all styling, plain CSS
- `db.sqlite3` — created automatically after `migrate` (nothing else to install)
