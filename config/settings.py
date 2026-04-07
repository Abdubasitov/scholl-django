from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-school-admin-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'school_site',
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

ROOT_URLCONF = 'config.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Jazzmin ────────────────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title":   "SchoolAdmin",
    "site_header":  "Управление сайтом школы",
    "site_brand":   "SchoolAdmin",
    "welcome_sign": "Добро пожаловать в панель управления сайтом школы",
    "copyright":    "SchoolAdmin — CMS для школ КР",
    "search_model": ["auth.User"],
    "topmenu_links": [
        {"name": "Открыть сайт",  "url": "/",                                              "new_window": True},
        {"name": "Заявки",        "url": "admin:school_site_applicationrequest_changelist"},
    ],
    "show_sidebar":        True,
    "navigation_expanded": True,
    # Иконки — только FontAwesome (встроены в Jazzmin)
    "icons": {
        "auth":                               "fas fa-users-cog",
        "auth.user":                          "fas fa-user",
        "auth.Group":                         "fas fa-users",
        "school_site.SchoolSettings":         "fas fa-school",
        "school_site.HeroSection":            "fas fa-home",
        "school_site.Statistic":              "fas fa-chart-bar",
        "school_site.AboutSection":           "fas fa-info-circle",
        "school_site.AboutFeature":           "fas fa-check-circle",
        "school_site.Program":                "fas fa-graduation-cap",
        "school_site.Teacher":                "fas fa-chalkboard-teacher",
        "school_site.Achievement":            "fas fa-trophy",
        "school_site.GalleryImage":           "fas fa-images",
        "school_site.ContactInfo":            "fas fa-address-book",
        "school_site.ApplicationRequest":     "fas fa-envelope-open-text",
    },
    "default_icon_parents":  "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "order_with_respect_to": [
        "school_site.SchoolSettings",
        "school_site.HeroSection",
        "school_site.Statistic",
        "school_site.AboutSection",
        "school_site.AboutFeature",
        "school_site.Program",
        "school_site.Teacher",
        "school_site.Achievement",
        "school_site.GalleryImage",
        "school_site.ContactInfo",
        "school_site.ApplicationRequest",
        "auth",
    ],
    "show_ui_builder":        False,
    "changeform_format":      "horizontal_tabs",
    "related_modal_active":   True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":       False,
    "footer_small_text":       True,
    "body_small_text":         True,
    "brand_colour":            "navbar-primary",
    "accent":                  "accent-primary",
    "navbar":                  "navbar-white navbar-light",
    "navbar_fixed":            True,
    "sidebar_fixed":           True,
    "sidebar":                 "sidebar-dark-primary",
    "sidebar_nav_child_indent":True,
    "sidebar_nav_compact_style": True,
    "theme":                   "default",
}
