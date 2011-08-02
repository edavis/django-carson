=============
django-carson
=============

django-carson makes it easy to collect tweets from a given set of
users as well as tweets using a specific hashtag.

You can see it in action on TweetNevada.com_.

.. _TweetNevada.com: http://tweetnevada.com

The basic idea is there are Twitter accounts you want to follow (e.g.,
Nevada lawmakers) and hashtags the "community" can use to engage in a
collective conversation (e.g., ``#nvleg``).  What django-carson aims
to do is make it easy to manage all of this.

Getting Started
---------------

#) Install django-carson::

    $ cd /tmp
    $ git clone git://github.com/edavis/django-carson.git # PyPI support coming soon
    $ mkvirtualenv --no-site-packages example_website
    $ cdsitepackages # or cd /path/to/virtualenv/lib/python2.7/site-packages
    $ ln -s /tmp/django-carson/carson .

#) Add ``carson`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        # ...
        'carson',
        # ...
    )

#) Configure your URLconf::

    # urls.py
    from django.conf.urls.defaults import patterns, include, url
    from django.contrib import admin
    admin.autodiscover()
    
    urlpatterns = patterns(
        '',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('carson.urls')),
    )

#) Create the appropriate OAuth tokens.  This is required to get
   access to the Twitter Streaming API.

   1) `Create a new application`_
   2) Click "Create my access token"

   Add these tokens to settings.py:

   ===================  ===============
       twitter.com        settings.py
   ===================  ===============
   Consumer key         CONSUMER_KEY
   Consumer secret      CONSUMER_SECRET
   Access token         TOKEN_KEY
   Access token secret  TOKEN_SECRET
   ===================  ===============

#) Via the `admin interface`_, add your accounts and hashtags.

#) Finally, run::

    $ ./manage.py consume_tweets

.. _Create a new application: https://dev.twitter.com/apps/new
.. _admin interface: http://localhost:8000/admin/carson/
