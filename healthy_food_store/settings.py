"""
Django settings for Healthy Bites & Refreshers
================================================
Edit values here to configure the project.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: change this key before deploying to production!
SECRET_KEY = 'django-insecure-healthy-bites-change-me-in-production'

DEBUG = True            # Set to False in production
ALLOWED_HOSTS = ['*']   # Restrict in production

# ---------------- Applications ----------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'accounts',
    'products',
    'cart',
    'orders',
    'feedbacks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'healthy_food_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # Global templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart_counter',  # cart badge in navbar
            ],
        },
    },
]

WSGI_APPLICATION = 'healthy_food_store.wsgi.application'

# ---------------- Database (SQLite) ----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------- Password validation ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------- Internationalisation ----------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# ---------------- Static & Media ----------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------- Auth redirects ----------------
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'products:home'
LOGOUT_REDIRECT_URL = 'products:home'

# ---------------- Email (console for development) ----------------
# Password-reset emails are printed to the terminal in development.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@healthybites.com'

# ---------------- Business settings ----------------
TAX_RATE = 0.13            # 13% VAT (Nepal)
DELIVERY_CHARGE = 100      # Flat Rs. 100 delivery
FREE_DELIVERY_ABOVE = 2000 # Free delivery for orders above Rs. 2000
LOYALTY_ORDER_COUNT = 5    # Promo generated on every 5th order
LOYALTY_DISCOUNT = 15      # 15% discount
