Django==1.3
psycopg2
-r django-carson/requirements.txt

Need to enable the admin interface

url(r'^', include('carson.urls')),

CONSUMER_KEY, CONSUMER_SECRET
TOKEN_KEY, TOKEN_SECRET in settings.py

https://dev.twitter.com/docs/streaming-api/methods

Limited to 400 hashtags and 5k accounts

TODO:: explain how to create oauth consumer/token

Private users can't be accessed
