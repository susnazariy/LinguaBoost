""" Django settings for linguaboost project """

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-p+8+j4daqd5ob%1*1%4w15yqrt@gw=rup%+=*!dlzq4sp9uwp7'

DEBUG = True

ALLOWED_HOSTS = []

REST_FRAMEWORK = {  # Djoser auth
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'linguaboost_application',
    'phonenumber_field',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'django_extensions',
    'admin_reorder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'linguaboost_settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'linguaboost_application/templates/')],
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

WSGI_APPLICATION = 'linguaboost_settings.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'linguaboost_db',
        'USER': 'postgres',
        'PASSWORD': '1111',
        'HOST': 'localhost',
        'PORT': '5433'
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "linguaboost_application/static"),
]

AUTH_USER_MODEL = 'linguaboost_application.CustomUser'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Reorder admin panel models

ADMIN_REORDER = (
    {
        'app': 'linguaboost_application',
        'models': (
                'linguaboost_application.WebsiteInformation',
                'linguaboost_application.CustomUser',
        ),
        'label': 'Linguaboost application'
    },
    {
        'app': 'linguaboost_application',
        'models': (
                'linguaboost_application.Course',
                'linguaboost_application.Lesson',
                'linguaboost_application.StudentCourse',
                'linguaboost_application.StudentApplication',
        ),
        'label': 'Teacher administration'
    },
    {
        'app': 'linguaboost_application',
        'models': (
                'linguaboost_application.OneManyTask',
                'linguaboost_application.FixSentenceTask',
                'linguaboost_application.TranslateWordTask',
                'linguaboost_application.SequenceTask',
                'linguaboost_application.AccordanceTask',
                'linguaboost_application.AccordanceTaskVariant',
        ),
        'label': 'Tasks'
    },
    {
        'app': 'linguaboost_application',
        'models': (
                'linguaboost_application.DiscussionExercise',
                'linguaboost_application.ReadingExercise',
                'linguaboost_application.ListeningExercise',
                'linguaboost_application.RulesExercise',
                'linguaboost_application.VocabularyExercise',
                'linguaboost_application.VocabularyWord',
        ),
        'label': 'Exercises'
    },
{
        'app': 'linguaboost_application',
        'models': (
                'linguaboost_application.LessonTestResult',
                'linguaboost_application.CourseFinalTestResult',
        ),
        'label': 'Tests'
    },
)
