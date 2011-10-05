=============
django-carson
=============

django-carson makes it easy to store and display tweets from a set of
users or tweets about a given topic.

For an idea of how django-carson can be used, take a look at
TweetNevada_.

The basic idea is you'll have a set of Twitter accounts you want to
follow (e.g., Nevada lawmakers) and a set of common hashtags and/or
keywords (e.g., ``#nvleg``) used by the community to engage in a
collective conversation about a given topic.  When combined on the
same page, you get a very interesting and dynamic conversation taking
place.

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

   First, `create a new application`_.  Then, click "Create my access
   token."

   Add the following values to ``settings.py``

   - "Consumer key" → ``CONSUMER_KEY``
   - "Consumer secret" → ``CONSUMER_SECRET``
   - "Access token" → ``TOKEN_KEY``
   - "Access token secret" → ``TOKEN_SECRET``

#) Via the `admin interface`_, add your accounts and hashtags/keywords.

   **Note:** You're not required to add both accounts and
   hashtags/keywords.  If you want, you could design a site that only
   stored hashtag mentions or only tweets sent by your given set of
   users.

#) If you added any accounts, you must either run ``./manage.py
   lookup_twitter_ids`` or use the "Lookup Twitter IDs" admin action
   before the next step will work.  If you only added hashtags or
   keywords, you don't need to do this.

#) Finally, run::

     $ ./manage.py get_tweets

   This will open a connection to the Twitter Streaming API and
   immediately after one of your accounts posts a tweet or a
   tweet is created mentioning one of your tags, that tweet will be
   stored.

Usage
-----

django-carson is only a bridge between Django and the Twitter
Streaming API.  It is the web developer's job to wire up the views and
templates needed to actually display the data.

The main entry point for any developer using ``carson`` is likely to
be ``carson.models.Tweet``.  This model holds all tweets stored with
``get_tweets``.

Each ``carson.models.Tweet`` object has four attributes:

  **account**
    A ForeignKey pointing to the ``carson.models.Account`` that
    created the tweet, if applicable.  Will be ``None`` if the tweet
    didn't come from an account listed in ``carson.models.Account``.

  **timestamp**
    The UTC timestamp of the tweet.

  **status_id**
    The unique status id for each tweet.  This is also in data['id'],
    but this allows an index to be created for it.

  **data**
    Stores the complete JSON_ object associated with the tweet.  You
    can see what all is included in this attribute `here <https://dev.twitter.com/docs/api/1/get/statuses/show/%3Aid>`_.

Attached to ``carson.models.Tweet`` are three managers:

  **objects**
    Returns a ``QuerySet`` of all tweets

  **trusted**
    Returns only the tweets associated with a
    ``carson.models.Account``.  In other words, ``Tweet.account != None``.

  **untrusted**
    Returns only the tweets not associated with a
    ``carson.models.Account``.  In other words, ``Tweet.account ==
    None``.

A simple index view exists in ``carson.views.index`` which grabs the
20 most recent trusted and untrusted tweets and renders
``carson/index.html`` (with the context variables ``trusted`` and
``untrusted``).  Might be useful if your website isn't too complex.

If you seem to be having problems accessing the Twitter API, you can
set ``HTTP_DEBUG`` to ``True`` in ``settings.py``.  By default it is
``False``.

.. _create a new application: https://dev.twitter.com/apps/new
.. _admin interface: http://localhost:8000/admin/carson/
.. _Twitter Streaming API: https://dev.twitter.com/docs/streaming-api
.. _TweetNevada: http://tweetnevada.com/
.. _JSON: http://en.wikipedia.org/wiki/JSON
.. _South: http://south.aeracode.org/

Changelog
---------

**0.2 (October 5th, 2011)**
  - Use SSL for Streaming and REST APIs
  - Document and test some utility methods
  - Use `requests <http://requests.readthedocs.org/en/latest/>`_ for
    REST API calls

**0.1 (August 9th, 2011)**
  - Initial release
