from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'carson',                      # Or path to database file if using sqlite3.
    }
}

from twitter_credentials import *
