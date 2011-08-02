=============
django-carson
=============

django-carson is a Django app that makes it easy to collect tweets
from a given set of users as well as tweets containing a specific
hashtag or keyword.

You can see it in action on TweetNevada.com_.

.. _TweetNevada.com: http://tweetnevada.com

The idea is there are Twitter accounts you want to follow (*e.g.,*
Nevada lawmakers) and hashtags or keywords the community uses to
engage in a collective conversation (*e.g.,* ``#nvleg``).  All public
tweets from your "whitelisted" accounts are displayed, and all public
tweets containing your hashtags/keywords also captured and displayed.

By combing the two, you create a "running conversation" about a given
topic.  In the case of TweetNevada, it focused on Nevada's 2011 Legislative
Session.

Getting Started
---------------

#) Install django-carson::

    $ mkvirtualenv --no-site-packages example_website
    $ pip install django-carson

#) Add ``carson`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        # ...
        'carson',
        # ...
    )

#) Configure your URLconf::

    urlpatterns = patterns(
        '',
        # ...
        url(r'^', include('carson.urls')),
    )

#) Create the appropriate OAuth tokens.  This is required to get
   access to the Twitter Streaming API.

   1) `Create a new application`_
   2) Click "Create my access token"

   Add these tokens to settings.py:

   - Consumer key --> CONSUMER_KEY
   - Consumer secret --> CONSUMER_SECRET
   - Access token --> TOKEN_KEY
   - Access token secret --> TOKEN_SECRET

#) Via the `admin interface`_, add your accounts and hashtags.

#) After adding any accounts, you must either use the "Lookup Twitter
   IDs" admin action or ``./manage.py lookup_twitter_ids`` to populate
   each account with its Twitter ID.

#) Finally, run::

    $ ./manage.py get_tweets

.. _Create a new application: https://dev.twitter.com/apps/new
.. _admin interface: http://localhost:8000/admin/carson/
