"""
Open a connection to Twitter's streaming API and track any and all
tweets either from a whitelisted user or containing a given hashtag.
"""

import sys
from django.core.management.base import BaseCommand, CommandError
from carson.models import Account, Tag
from carson.utils import Streamer

class Command(BaseCommand):
    help = "Consume twitter updates"

    def handle(self, *args, **kwargs):
        accounts = Account.objects.all()
        tags = Tag.objects.all()

        follow = ",".join(map(str, accounts.values_list('twitter_id', flat=True)))
        track = ",".join(tags.values_list('name', flat=True))

        # If you pass an empty value to Streamer.main(), it doesn't work
        params = {}
        if follow:
            params['follow'] = follow
            sys.stdout.write("Following: '%s'\n" % follow)
        if track:
            params['track'] = track
            sys.stdout.write("Tracking:  '%s'\n" % track)

        sys.stdout.flush()

        streamer = Streamer()
        streamer.main(**params)
