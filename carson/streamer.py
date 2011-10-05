import sys
import pytz
import json
import urllib
import httplib
from datetime import datetime
from django.conf import settings
from carson.utils import (
    generate_signed_request, get_credentials, write_update, http_debug)

class Streamer(object):
    def __init__(self):
        credentials = get_credentials()
        self.consumer = credentials['consumer']
        self.token    = credentials['token']
        self.url      = "https://stream.twitter.com/1"

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
        kwargs['delimited'] = 'length'

        url = self.url + "/statuses/filter.json"
        data = generate_signed_request(url, kwargs)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        connection = httplib.HTTPSConnection("stream.twitter.com")
        if http_debug():
            connection.set_debuglevel(1)

        connection.request(
            method = "POST",
            url = "/1/statuses/filter.json",
            body = urllib.urlencode(data),
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
                    write_update("Added #%d" % update['id'], newline=True)

            else:
                write_update("Ping!")
