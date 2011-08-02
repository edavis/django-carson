import pytz
import json
import time
import urllib
import pprint
import locale
import httplib
import oauth2 as oauth
from datetime import datetime
from django.conf import settings

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
            c = self.response.read(1)
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
        connection.set_debuglevel(1)

        connection.request(method  = "POST",
                           url     = "/%d/statuses/filter.json" % VERSION,
                           body    = urllib.urlencode(request),
                           headers = headers)

        self.response = connection.getresponse()

        # Placed here because otherwise it would trigger a circular-import
        from carson.models import Tweet

        while True:
            length = self._get_length()
            if length:
                update = self.response.read(length)
                Tweet.add(update)
            else:
                continue
