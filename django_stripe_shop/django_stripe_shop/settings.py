import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "django_stripe_shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "store" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": ["django.template.context_processors.request",
                                           "django.contrib.auth.context_processors.auth",
                                           "django.template.context_processors.debug",
                                           "django.template.context_processors.i18n",
                                           "django.template.context_processors.media",
                                           "django.template.context_processors.static",
                                           "django.template.context_processors.tz",
                                           "django.contrib.messages.context_processors.messages",]},
    },
]

WSGI_APPLICATION = "django_stripe_shop.wsgi.application"

# Postgres DB (edit these)
DATABASES = {
    "default": {
        "ENGINE":"django.db.backends.sqlite3", 
        "NAME": BASE_DIR/"db.sqlite3"}}


# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "store" / "static"]

STRIPE_PUBLIC_KEY = "pk_test_your_real_key_here"
STRIPE_SECRET_KEY = "sk_test_your_real_key_here"



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
