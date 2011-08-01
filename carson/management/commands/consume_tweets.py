"""
Open a connection to Twitter's streaming API and track any and all
tweets either from a whitelisted user or containing a given hashtag.
"""

from django.core.management.base import BaseCommand, CommandError
from carson.models import Account, Tag
from carson.utils import Streamer

class Command(BaseCommand):
    help = "Consume twitter updates"

    def handle(self, *args, **kwargs):
        import random
        follow = ",".join(str(n) for n in random.sample(xrange(10000000, 20000000), 100))
        track = ",".join(["#dearyoungself"])

        streamer = Streamer()
        streamer.main(follow=follow, track=track)
