"""
Open a connection to Twitter's streaming API and track any and all
tweets either from a whitelisted user or containing a given hashtag.
"""

import sys
from django.core.management.base import BaseCommand, CommandError
from carson.models import Account, Tag
from carson.streamer import Streamer

class Command(BaseCommand):
    help = "Consume twitter updates"

    def handle(self, *args, **kwargs):
        accounts = Account.objects.all()
        tags = Tag.objects.all()

        # Alert when an Account doesn't have its twitter_id set
        empty_ids = accounts.filter(twitter_id=None)
        if empty_ids:
            sys.stderr.write("Missing Twitter IDs for:\n")
            for account in empty_ids:
                sys.stderr.write("\t- %s\n" % account.twitter_username)
            sys.stderr.write("Run ./manage.py lookup_twitter_ids or select \"Lookup Twitter IDs\" in the admin.\n")
            raise SystemExit

        follow = ",".join(map(str, accounts.values_list('twitter_id', flat=True)))
        track = ",".join(tags.values_list('name', flat=True))

        params = {}

        if follow: params['follow'] = follow
        if track: params['track'] = track

        streamer = Streamer()
        streamer.main(**params)
