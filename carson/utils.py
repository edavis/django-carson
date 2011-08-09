import sys
import pytz
import json
import time
import urllib
import pprint
import locale
import httplib
import httplib2
import oauth2 as oauth
from datetime import datetime
from django.conf import settings

def write_update(msg, handler=sys.stdout, newline=False):
    """
    Write a line to ``handler``, using an ANSI escape code
    so everything gets cleanly overwritten.
    """
    nl = "\n" if newline else "\r"
    handler.write("\033[2K%s%s" % (msg, nl))
    handler.flush()

def lookup_twitter_ids(queryset, username_field="twitter_username"):
    usernames = queryset.values_list(username_field, flat=True)[:100]
    usernames = ",".join(usernames)

    http = httplib2.Http('/tmp/httplib2/')
    if getattr(settings, 'HTTP_DEBUG', False):
        httplib2.debuglevel = 1

    consumer = oauth.Consumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    token    = oauth.Token(settings.TOKEN_KEY, settings.TOKEN_SECRET)

    params = {
        "oauth_version"      : "1.0",
        "oauth_nonce"        : oauth.generate_nonce(),
        "oauth_timestamp"    : int(time.time()),
        "oauth_token"        : token.key,
        "oauth_consumer_key" : consumer.key,

        "screen_name"        : usernames,
        "include_entities"   : 0,
    }

    url = "http://api.twitter.com/1/users/lookup.json"
    request = oauth.Request("POST", url, params)
    request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)

    response, content = http.request(
        uri = url,
        method = "POST",
        body = urllib.urlencode(request),
        headers = {"Content-Type": "application/x-www-form-urlencoded"},
    )

    response = json.loads(content)

    updated = 0
    for obj in response:
        lookup = {username_field: obj["screen_name"]}
        account = queryset.model.objects.get(**lookup)
        account.twitter_id = obj["id"]
        account.save()
        updated += 1

    return updated

def parse_created_at(created_at):
    t = time.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
    return datetime(*t[:6], tzinfo=pytz.utc)

ENDPOINT, VERSION = "stream.twitter.com", 1

class Streamer(object):
    def __init__(self):
        self.consumer = oauth.Consumer(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        self.token    = oauth.Token(settings.TOKEN_KEY, settings.TOKEN_SECRET)
        self.url      = "http://%s/%d" % (ENDPOINT, VERSION)

    def _get_length(self):
        buf = ""

        while True:
            try:
                c = self.response.read(1)
            except httplib.HTTPException:
                continue
            except KeyboardInterrupt:
                sys.stderr.write("\nExiting...\n")
                raise SystemExit

            if c == '\n':
                break
            else:
                buf += c

        buf = buf.strip()
        if buf and buf.isdigit():
            return int(buf)

    def main(self, **kwargs):
        params = {
            "delimited"          : "length",
            "oauth_version"      : "1.0",
            "oauth_nonce"        : oauth.generate_nonce(),
            "oauth_timestamp"    : int(time.time()),
            "oauth_token"        : self.token.key,
            "oauth_consumer_key" : self.consumer.key,
        }

        # Include any track and/or follow parameters
        params.update(kwargs)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Populate params with needed oauth stuff
        request = oauth.Request("POST", self.url + "/statuses/filter.json", parameters=params)
        request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)

        # Configure a raw HTTP connection to stream.twitter.com
        connection = httplib.HTTPConnection(ENDPOINT)
        if getattr(settings, 'HTTP_DEBUG', False):
            connection.set_debuglevel(1)

        connection.request(method  = "POST",
                           url     = "/%d/statuses/filter.json" % VERSION,
                           body    = urllib.urlencode(request),
                           headers = headers)

        self.response = connection.getresponse()

        # Placed here because otherwise it would trigger a circular-import
        from carson.models import Tweet, Account

        twitter_ids = Account.objects.values_list('twitter_id', flat=True)

        while True:
            length = self._get_length()
            if length:
                update = self.response.read(length)
                update = json.loads(update)

                if 'in_reply_to_status_id' in update:
                    Tweet.add(update, twitter_ids)

                    now = datetime.utcnow()
                    now = now.replace(tzinfo=pytz.utc)
                    timestamp = now.astimezone(pytz.timezone(settings.TIME_ZONE))
                    write_update("Added #%d (%s)" % (update['id'], timestamp.strftime("%D %r")), newline=True)

            else:
                now = datetime.utcnow()
                now = now.replace(tzinfo=pytz.utc)
                timestamp = now.astimezone(pytz.timezone(settings.TIME_ZONE))

                write_update("Ping! (%s)" % timestamp.strftime("%D %r"))
