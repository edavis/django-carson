=============
django-carson
=============

django-carson makes it easy to store tweets sent by a given set of
users along with tweets containing a specific hashtag or keyword.

To get an idea of the uses of django-carson, take a look at
TweetNevada_.

The basic idea is you'll have a set of Twitter accounts you want to
follow (e.g., Nevada lawmakers) and a set of common hashtags and/or
keywords (e.g., ``#nvleg``) used by the community to engage in a
collective conversation about a given topic.  When the two components
are combined on the same page, you get a very dynamic and interesting
conversation taking place.

Getting Started
---------------

#) Install django-carson::

     $ mkvirtualenv --no-site-packages example_website
     $ pip install django-carson

#) Add ``carson`` to your ``INSTALLED_APPS``

#) Create the database tables with ``syncdb`` (or ``migrate carson`` if you
   use South_)

#) To access the `Twitter Streaming API`_, you must first create the
   appropriate tokens.

   First, `create a new application`_.  Then, click "Create my access token."

   Once done, add the values of "Consumer Key," "Consumer secret,"
   "Access token," and "Access token secret" to ``settings.py`` as
   ``CONSUMER_KEY``, ``CONSUMER_SECRET``, ``TOKEN_KEY``, and
   ``TOKEN_SECRET``, respectively.

#) Via the `admin interface`_, add your accounts and hashtags/keywords.

   Note: You're not required to add both accounts and
   hashtags/keywords.  If you wanted, you could design a site that
   only listened for hashtag mentions or only stored tweets sent by a
   given set of users.

#) If you added any accounts, you must either run ``./manage.py
   lookup_twitter_ids`` or use the "Lookup Twitter IDs" admin action
   before the next step will work.

#) Finally, run::

     $ ./manage.py get_tweets

   This will open a connection to the `Twitter Streaming API`_ and
   immediately after one of your accounts posts a tweet or a
   tweet is created mentioning one of your tags, that tweet will be
   stored.

Usage
-----

django-carson only exists as a simple bridge between Django and the
Twitter Streaming API.  As such, it is up to the web developer to
wire up the views and templates needed to display the data.

The main entry point for any developer using carson is likely to be
the ``Tweet`` class in models.py_.  This is the model that holds all
the tweets stored with ``get_tweets`` above.

Each ``Tweet`` object has two attributes:

  - **account**: A ForeignKey that points to the ``Account`` object
    that created the tweet, if applicable, otherwise ``None``.

  - **data**: Stores the complete, decoded JSON_ object associated with the
    tweet.  As this value will be a regular dictionary, Django's
    `template syntax`_ will be able to access everything_ about the
    status update.

Attached to this ``Tweet`` class are three managers:

  - ``objects``: all tweets
  - ``trusted``: tweets from accounts created in the admin (i.e.,
    ``Tweet.account != None``)
  - ``untrusted``: tweets mentioning your tags (i.e.,
    ``Tweet.account == None``)

A simple index view exists in ``carson.views.index`` which grabs the
20 most recent trusted and untrusted tweets and renders
``carson/index.html`` (with the context variables ``trusted`` and
``untrusted``).  Might be useful if your website isn't too complex.

.. _create a new application: https://dev.twitter.com/apps/new
.. _admin interface: http://localhost:8000/admin/carson/
.. _Twitter Streaming API: https://dev.twitter.com/docs/streaming-api
.. _TweetNevada: http://tweetnevada.com/
.. _models.py: https://github.com/edavis/django-carson/tree/master/carson/models.py
.. _views.py: https://github.com/edavis/django-carson/tree/master/carson/views.py
.. _JSON: http://en.wikipedia.org/wiki/JSON
.. _template syntax: https://docs.djangoproject.com/en/1.3/topics/templates/#variables
.. _everything: https://dev.twitter.com/docs/api/1/get/statuses/show/%3Aid
.. _South: http://south.aeracode.org/
