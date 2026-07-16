# Portfolio Backend (Django + DRF + SQLite)

A Django REST Framework API that serves the portfolio's content, plus
Django's built-in admin at `/admin` for editing everything after deploy —
no code changes needed.

## What's inside
- `portfolio_backend/` – Django project (settings, URLs, WSGI/ASGI)
- `content/` – the app: models, admin registrations, DRF serializers/views
- `content/management/commands/seed_data.py` – one-time command that creates
  your admin login and loads the content that was on the original static
  site, so the site looks the same on first run
- `db.sqlite3` – the SQLite database file, shipped already migrated and
  seeded so the API works immediately
- `api/index.py` + `vercel.json` – lets this Django app run on Vercel

## 1. Local setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then edit .env - see below
```

Edit `.env`:
- `SECRET_KEY` – any long random string
- `DEBUG` – `True` for local dev
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` – your admin login (used once, by `seed_data`)
- `CORS_ORIGINS` – your frontend's URL(s), comma-separated

The repo already ships a migrated + seeded `db.sqlite3`, so you can run the
server immediately:
```bash
python manage.py runserver
```
Visit `http://localhost:8000/admin` and log in with `admin` / the password
from `seed_data.py`'s defaults, **or** reset it yourself:
```bash
python manage.py changepassword admin
```

### Starting from a totally fresh database instead
If you'd rather start clean:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_data      # creates admin login + loads starter content
```

## 2. Editing content
Go to `http://localhost:8000/admin` (or your deployed URL + `/admin`), log
in, and you'll see a section for every content type:
- **Site Settings** – profile, contact info, social links, homepage stats,
  research interests, skills, personal info, teaching info, footer (all on
  one page, since there's only ever one of these)
- **Education, Experience, Publications, Projects, Certifications, Awards,
  Activities, Gallery Events (with photo rows), Courses, Blog Posts,
  References** – standard add/edit/delete lists, each with a "Sort order"
  column you can edit inline

Changes appear on the live site as soon as the page reloads — the frontend
fetches fresh data from the API on every load.

## 3. Deploy to Vercel via GitHub
1. Push this `backend/` folder to its own GitHub repository.
2. Go to https://vercel.com → **Add New → Project** → import that repository.
   Vercel will detect `vercel.json` and use the Python runtime automatically.
3. In the project's **Settings → Environment Variables**, add `SECRET_KEY`,
   `DEBUG=False`, `ALLOWED_HOSTS` (your Vercel domain), and `CORS_ORIGINS`
   (your frontend's URL).
4. Deploy. You'll get a URL like `https://portfolio-backend.vercel.app`.
5. Visit `https://portfolio-backend.vercel.app/admin` to manage content, and
   use `https://portfolio-backend.vercel.app/api` as the `API_BASE` in the
   frontend's `assets/js/config.js`.

### ⚠️ Important: SQLite + Vercel = not permanent storage
Vercel serverless functions run on a **read-only, ephemeral filesystem** —
only `/tmp` is writable, and it's wiped on every cold start / redeploy. This
project copies the committed `db.sqlite3` into `/tmp` on startup so the app
works out of the box, but **any edits you make through `/admin` while
deployed on Vercel will disappear the next time the function cold-starts**
(which can happen at any time, especially after periods of inactivity).

This is fine if you mainly edit locally and redeploy (commit an updated
`db.sqlite3`), or want a live read-only demo. If you want to **edit content
directly on the live site and have it stick**, pick one of these instead:
- **Easiest fix:** deploy to a host with a real persistent disk — **Render**
  or **Railway** both support Django + SQLite out of the box with a
  persistent volume, and their free tiers are simple to set up.
- **Stay on Vercel:** swap SQLite for a free hosted Postgres (Vercel
  Postgres, Neon, or Supabase) — same Django code, just change
  `DATABASES` in `settings.py` to point at it (Django's ORM makes this a
  small change).

## API reference
Everything is public/read-only (all editing happens through `/admin`):

| Path | Description |
|---|---|
| `/api/settings` | Singleton profile/site content |
| `/api/education` | List of education entries |
| `/api/experience` | List of work/research experience entries |
| `/api/publications` | List of publications |
| `/api/projects` | List of projects |
| `/api/certifications` | List of certifications |
| `/api/awards` | List of awards |
| `/api/activities` | List of co-curricular activities |
| `/api/gallery` | List of gallery events, each with nested `photos` |
| `/api/courses` | List of teaching courses |
| `/api/blog` | List of blog posts |
| `/api/references` | List of references |
| `/api/health` | Health check |

Each collection also supports `/api/<name>/<id>` for a single item.
