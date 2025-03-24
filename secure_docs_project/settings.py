"""
Paramètres Django pour le projet secure_docs_project.

Généré par 'django-admin startproject' en utilisant Django 5.1.3.

Pour plus d'informations sur ce fichier, voir
https://docs.djangoproject.com/en/5.1/topics/settings/

Pour la liste complète des paramètres et leurs valeurs, voir
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from cryptography.fernet import Fernet

# Construction des chemins dans le projet comme ceci : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Paramètres de démarrage rapide - non adaptés pour la production
# Voir https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# AVERTISSEMENT DE SÉCURITÉ : gardez la clé secrète utilisée en production secrète !
SECRET_KEY = "django-insecure-+3$%@b9&498hf+!t1+pa3%xf!bry3_rku+9#ibmh5^pamsi&$u"

# AVERTISSEMENT DE SÉCURITÉ : ne pas exécuter avec le debug activé en production !
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Définition des applications

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "documents",
    "crispy_forms",
    "social_django",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "secure_docs_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "secure_docs_project.wsgi.application"


# Base de données
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SecurDoc',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '8889',
    }
}


# Validation des mots de passe
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalisation
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Fichiers statiques (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Paramètres Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Paramètres de connexion
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = 'documents:list'
LOGOUT_REDIRECT_URL = '/'

# Paramètres de chiffrement
ENCRYPTION_KEY = b'Jgc9inqkGRk58nirpkvRNRHj0ReybTvjtSoI2pKke5Q='

# Pour générer une nouvelle clé, décommentez et exécutez ceci une fois, puis copiez la clé imprimée :
# if __name__ == '__main__':
#     print(Fernet.generate_key())

# Backends d'authentification
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Paramètres d'authentification sociale
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Paramètres OAuth2 Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''  # Ajoutez votre ID client Google ici
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''  # Ajoutez votre secret client Google ici
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

# Paramètres supplémentaires d'authentification sociale
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'documents:list'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Pipeline pour obtenir des informations utilisateur supplémentaires
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Type de champ de clé primaire par défaut
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
