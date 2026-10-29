# ApplyFlow

ApplyFlow is a web application for keeping internship and job applications organized in one place. Users can create an account, maintain a profile, track application statuses, and search their application list.

**Live website:** https://applyflow-kjyi.onrender.com

## Features

- User signup, login, and logout
- Editable user profile
- Add, view, edit, and delete applications
- Track company, role, location, job type, status, application date, deadline, job link, and notes
- Search by company, role, or location
- Filter applications by status
- Dashboard with application counts
- Responsive layout for desktop and mobile screens

## Tech stack

- **Frontend:** HTML, CSS, Django Templates
- **Backend:** Python, Django
- **Database:** SQLite for local development; PostgreSQL when `DATABASE_URL` is configured
- **Deployment:** Render
- **Database hosting:** Neon PostgreSQL
- **Version control:** Git and GitHub

## Run locally

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd ApplyFlow
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Create database tables

```powershell
python manage.py migrate
```

### 5. Start the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Production configuration

The deployed app uses environment variables. Configure them in the hosting service rather than committing them to the repository.

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Private Django secret key |
| `DEBUG` | Set to `False` in production |
| `DATABASE_URL` | PostgreSQL connection string for the production database |
| `ALLOWED_HOSTS` | Optional comma-separated hostnames; Render's external hostname is also read automatically |
| `CSRF_TRUSTED_ORIGINS` | Optional comma-separated HTTPS origins |

For deployment, install dependencies from `requirements.txt`, collect static files, apply migrations, and start the app with a production WSGI server. The current Render start command is:

```bash
gunicorn config.wsgi:application --workers 1 --threads 2 --timeout 120
```

## Project structure

```text
ApplyFlow/
├── applications/
│   ├── migrations/
│   ├── static/applications/style.css
│   ├── templates/
│   │   ├── applications/
│   │   └── registration/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Notes

- Do not commit `.env` files, database passwords, Django secret keys, `.venv/`, or the local `db.sqlite3` file.
- The live database is separate from the local SQLite database. Local records do not automatically appear on the deployed website.
- This project is intended as a student web-technology project and can be extended with reminders, interview scheduling, analytics, and AJAX-based search.
