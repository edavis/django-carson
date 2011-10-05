import sys
import pytz
import json
import time
import urllib
import pprint
import locale
import httplib
import requests
import oauth2 as oauth
from datetime import datetime
from django.conf import settings

def http_debug():
    return getattr(settings, 'HTTP_DEBUG', False)

if http_debug():
    requests.settings.verbose = sys.stderr

def write_update(msg, handler=sys.stdout, newline=False):
    """
    Write a line to ``handler``, using an ANSI escape code
    so everything gets cleanly overwritten.
    """
    now = datetime.utcnow()
    now = now.replace(tzinfo=pytz.utc)
    now = now.astimezone(pytz.timezone(settings.TIME_ZONE))

    nl = "\n" if newline else "\r"
    handler.write("\033[2K%s (%s)%s" % (msg, now.strftime("%D %r"), nl))
    handler.flush()

def get_credentials():
    return dict(
        consumer = oauth.Consumer(settings.CONSUMER_KEY,
                                  settings.CONSUMER_SECRET),
        token = oauth.Token(settings.TOKEN_KEY, settings.TOKEN_SECRET)
    )

def generate_signed_request(url, body):
    """
    Do the generic oauth signing needed for the REST and Streaming
    APIs.

    This function returns a dict that is passed as the body of a POST
    call.
    """
    credentials = get_credentials()
    consumer = credentials['consumer']
    token = credentials['token']

    params = {
        "oauth_version"      : "1.0",
        "oauth_nonce"        : oauth.generate_nonce(),
        "oauth_timestamp"    : int(time.time()),
        "oauth_token"        : token.key,
        "oauth_consumer_key" : consumer.key,
    }
    params.update(body)

    request = oauth.Request("POST", url, params)
    request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)
    return request

def twitter_api_call(method, body):
    """
    Call the given Twitter REST API method with a body.
    """
    assert method.endswith(".json"), "It's 2011, use JSON"
    url = "https://api.twitter.com/1/" + method
    data = generate_signed_request(url, body)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)

    if response.ok and response.content:
        return json.loads(response.content)
    else:
        response.raise_for_status()

def lookup_twitter_ids(queryset, username_field="twitter_username"):
    """
    Given a QuerySet of Accounts, fill in the ``twitter_id`` field.

    This saves us from having to call /users/lookup.json each time we
    create the Streamer but also doesn't force the website operator to
    find each Twitter ID (which can be cumbersome) when they add the
    account.

    We *could* do something like this when the Account object is
    created, but we're good people so bulk lookups are better.
    """
    usernames = queryset.values_list(username_field, flat=True)[:100]
    body = dict(
        screen_name = ",".join(usernames),
        include_entities = 0,
    )
    response = twitter_api_call("/users/lookup.json", body)
    return queryset.model.attach_twitter_ids(response)

def parse_created_at(created_at):
    """
    Coerce Twitter datetimes into a Python datetime object and set its
    timezone to UTC.
    """
    assert "+0000" in created_at, "Not in UTC, something might be wrong."
    t = time.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
    return datetime(*t[:6], tzinfo=pytz.utc)
