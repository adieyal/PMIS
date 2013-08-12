from base import *

########## TEST SETTINGS
TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = SITE_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"
########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
INSTALLED_APPS += (
    'django_coverage',
    'django_jenkins',
    'django_hudson',
)

PROJECT_APPS = (
    'project.apps.project',
    'project.apps.api',
)

COVERAGE_REPORT_HTML_OUTPUT_DIR = normpath(join(SITE_ROOT, 'coverage'))
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
