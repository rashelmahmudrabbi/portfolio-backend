# Portfolio Backend (Django + DRF)

A Django REST Framework API that serves all the content for the portfolio
site, plus Django's built-in admin panel at `/admin` for editing everything
after deploy — no code changes needed to update your CV, projects,
publications, etc.

**Live API:** `https://portfolio-backend-oz0v.onrender.com/api`
**Admin panel:** `https://portfolio-backend-oz0v.onrender.com/admin`

---

## What's inside

```
portfolio-backend/
├── portfolio/              # Django project (settings, root urls, WSGI/ASGI)
├── content/                 # the app: models, admin registrations, DRF views/serializers
│   └── management/commands/seed_data.py   # loads starter content + creates admin login
├── staticfiles/              # collected static files (generated, not hand-edited)
├── db.sqlite3                 # local-dev database (NOT used in production — see below)
├── manage.py
├── requirements.txt
├── runtime.txt                # pins Python version for deployment
└── .env.example                # template for local environment variables
```

## Tech stack

- **Django 5** + **Django REST Framework** — API
- **django-cors-headers** — allows the frontend's origin to call this API
- **whitenoise** — serves static/admin files without a separate static host
- **gunicorn** — production WSGI server
- **dj-database-url** + **psycopg2-binary** — lets one `DATABASES` config
  work with either local SQLite or a hosted Postgres instance via a single
  `DATABASE_URL` environment variable

---

## 1. Local setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then edit .env — see below
```

Edit `.env`:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | any long random string |
| `DEBUG` | `True` for local dev |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | admin login created by `seed_data` |
| `DATABASE_URL` | leave unset locally — falls back to `db.sqlite3` automatically |

Run the server:

```bash
python manage.py migrate
python manage.py seed_data       # creates admin login + loads starter content
python manage.py runserver
```

Visit `http://localhost:8000/admin` to log in and start editing content.

---

## 2. Editing content

Log in to `/admin` (locally or on the live Render URL) and you'll find a
section for every content type:

- **Site Settings** — profile, contact info, social links, homepage stats,
  research interests, skills, personal info, teaching info, footer (a
  singleton — there's only ever one)
- **Education, Experience, Publications, Projects, Certifications, Awards,
  Activities, Gallery Events (with photo rows), Courses, Blog Posts,
  References** — standard add/edit/delete lists, each with a **Sort order**
  field you can edit inline

The frontend fetches fresh data from this API on every page load, so
changes made in `/admin` appear on the live site immediately — no
redeploy of the frontend needed.

---

## 3. Deployment (Render)

This backend is deployed on **Render** as a Web Service, backed by a
**Render PostgreSQL** instance (SQLite doesn't persist on most cloud hosts
since their filesystems are ephemeral/read-only between deploys).

**Build command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start command:**
```bash
gunicorn portfolio.wsgi:application
```

**Environment variables set in Render's dashboard:**

| Key | Value |
|---|---|
| `SECRET_KEY` | a long random string, generated for production |
| `DEBUG` | `False` |
| `DATABASE_URL` | Render Postgres **Internal Database URL** |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | used once by `seed_data`, if run |

### Redeploying

Render redeploys automatically on every push to `main`. Watch the deploy
logs in the Render dashboard to confirm `migrate` and `collectstatic`
complete without errors.

### Creating/resetting the admin user on Render

Open the **Shell** tab on the Render service:
```bash
python manage.py createsuperuser
```
or, to also (re)load the starter content:
```bash
python manage.py seed_data
```

---

## 4. CORS

Only origins listed in `CORS_ALLOWED_ORIGINS` (in `settings.py`) may call
this API from a browser. Currently allowed:

- `https://rashelmahmudrabbi.github.io` (production frontend)
- `http://localhost:5500` / `http://127.0.0.1:5500` (local frontend dev)

If the frontend ever moves to a new domain, add it here and redeploy.

---

## API reference

Routes use **no trailing slash** (`/api/education`, not `/api/education/`)
to match the frontend's existing fetch calls.

| Path | Method | Description |
|---|---|---|
| `/api/health` | GET | Health check |
| `/api/settings` | GET | Singleton profile/site content |
| `/api/education` | GET | List of education entries |
| `/api/experience` | GET | List of work/research experience entries |
| `/api/publications` | GET | List of publications |
| `/api/projects` | GET | List of projects |
| `/api/certifications` | GET | List of certifications |
| `/api/awards` | GET | List of awards |
| `/api/activities` | GET | List of co-curricular activities |
| `/api/gallery` | GET | List of gallery events, each with nested `photos` |
| `/api/courses` | GET | List of teaching courses |
| `/api/blog` | GET | List of blog posts |
| `/api/references` | GET | List of references |

Each collection also supports `/api/<name>/<id>` for a single item. All
endpoints are public/read-only — every edit happens through `/admin`.

---

## Troubleshooting

- **`NameError: BASE_DIR is not defined`** — the `DATABASES` block in
  `settings.py` must appear *after* `BASE_DIR = Path(__file__)...` in the
  file. Check for a stray duplicate `DATABASES` block above it.
- **Data disappears after a Render restart** — `DATABASE_URL` isn't set, so
  Django silently fell back to local SQLite, which doesn't persist. Confirm
  the env var is set in Render's dashboard.
- **Frontend gets CORS errors** — confirm the frontend's exact origin
  (protocol + domain, no trailing slash) is listed in
  `CORS_ALLOWED_ORIGINS`.