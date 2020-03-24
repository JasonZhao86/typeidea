from .base import *   # NOQA


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 以下是debug_toolbar的相关配置
INSTALLED_APPS += [
    'debug_toolbar',
    'pympler',
    # 'debug_toolbar_line_profiler',
    'silk',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'silk.middleware.SilkyMiddleware',
]

DEBUG_TOOLBAR_PANELS = [
    # 'djdt_flamegraph.FlamegraphPanel',
    # 'debug_toolbar_line_profiler.panel.ProfilingPanel',
    'pympler.panels.MemoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    # # Toolbar options
    # 'RESULTS_CACHE_SIZE': 3,
    # 'SHOW_COLLAPSED': True,
    # # Panel options
    # 'SQL_WARNING_THRESHOLD': 100,   # milliseconds
    'JQUERY_URL': 'https://code.jquery.com/jquery-2.2.4.js',   # 用于前端展示toolbar
}

INTERNAL_IPS = ['127.0.0.1', ]

