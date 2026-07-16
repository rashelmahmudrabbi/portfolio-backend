"""
Django settings for portfolio project.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

CORS_ALLOWED_ORIGINS = [
    "https://rashelmahmudrabbi.github.io",
    "http://localhost:5500",   # for local testing
]

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-only-insecure-secret-key-change-me')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*').split(',') if h.strip()]
# Vercel deployments serve every function from a *.vercel.app subdomain that
# changes per-deploy, plus your production domain if you attach one.
if os.environ.get('VERCEL'):
    ALLOWED_HOSTS.append('.vercel.app')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'content',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

# --- Database ---
# SQLite file lives inside the backend folder. On a normal host (your own
# machine, Render, Railway, a VPS, etc.) this file persists on disk between
# requests, so admin edits are saved permanently.
#
# IMPORTANT CAVEAT FOR VERCEL: Vercel serverless functions run on an
# ephemeral, read-only filesystem (only /tmp is writable, and it is wiped
# between invocations/cold starts). That means if you deploy this to Vercel
# as-is, writes made through the Django admin will NOT reliably persist.
# See the README for a Vercel-compatible workaround (copy the db to /tmp) or
# use a host with a persistent disk (Render/Railway/Fly.io) if you need real
# persistence in production.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('SQLITE_PATH', str(BASE_DIR / 'db.sqlite3')),
    }
}

if os.environ.get('VERCEL'):
    # Vercel's deployment bundle is read-only; only /tmp is writable, and it
    # is wiped on every cold start. Copy the committed db.sqlite3 into /tmp
    # so the app can at least start and accept writes for the lifetime of
    # this particular serverless instance. Those writes are NOT permanent -
    # see the README for why, and for options if you need real persistence.
    import shutil
    tmp_db = '/tmp/db.sqlite3'
    source_db = str(BASE_DIR / 'db.sqlite3')
    if not os.path.exists(tmp_db) and os.path.exists(source_db):
        shutil.copyfile(source_db, tmp_db)
    DATABASES['default']['NAME'] = tmp_db

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CORS ---
# Comma-separated list of frontend origins allowed to call this API,
# e.g. "https://your-frontend.vercel.app,http://localhost:5500"
_cors_origins = [o.strip() for o in os.environ.get('CORS_ORIGINS', '').split(',') if o.strip()]
if _cors_origins:
    CORS_ALLOWED_ORIGINS = _cors_origins
else:
    # No origins configured yet (e.g. first local run) - allow all so the
    # site still works; tighten this once you know your frontend's URL.
    CORS_ALLOW_ALL_ORIGINS = True

# --- REST framework ---
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_PAGINATION_CLASS': None,
}

# The frontend calls endpoints like /api/education (no trailing slash).
# Disable Django's automatic slash-redirect so those requests don't 301
# redirect (which breaks a lot of fetch/CORS setups).
APPEND_SLASH = False
