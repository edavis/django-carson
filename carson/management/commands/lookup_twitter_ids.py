import sys
from django.core.management.base import BaseCommand, CommandError
from carson.models import Account
from carson.utils import lookup_twitter_ids

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        accounts = Account.objects.filter(twitter_id=None)
        if accounts:
            updated = lookup_twitter_ids(accounts)
            sys.stdout.write("%d account(s) updated\n" % updated)
        else:
            sys.stdout.write("All accounts have their Twitter IDs\n")
        sys.stdout.flush()
