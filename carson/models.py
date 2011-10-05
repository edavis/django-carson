import json
import pytz
from django.db import models
from datetime import datetime
from django.conf import settings
from carson.utils import parse_created_at, write_update
from carson.managers import TrustedManager, UntrustedManager
from carson.json_field import JSONField

class Account(models.Model):
    twitter_username = models.CharField("Username", help_text="Minus the '@' sign", max_length=32)
    twitter_id = models.PositiveIntegerField("Twitter ID", editable=False, null=True)

    def __unicode__(self):
        return u"@%s" % self.twitter_username

    @classmethod
    def attach_twitter_ids(cls, response, username_field="twitter_username"):
        """
        For each account in the response, lookup the Account object
        and attach their Twitter ID to it.
        """
        updated = 0
        for obj in response:
            account = cls.objects.get(**{username_field: obj['screen_name']})
            account.twitter_id = obj['id']
            account.save()
            updated += 1
        return updated

class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

class Tweet(models.Model):
    account = models.ForeignKey(Account, null=True, related_name="tweets")
    timestamp = models.DateTimeField(db_index=True)
    status_id = models.BigIntegerField(db_index=True)
    data = JSONField()

    objects = models.Manager()
    trusted = TrustedManager()
    untrusted = UntrustedManager()

    class Meta:
        ordering = ("-timestamp", "-status_id")
        get_latest_by = "timestamp"

    @classmethod
    def add(cls, tweet, twitter_ids):
        values = {
            "data": tweet,
            "timestamp": parse_created_at(tweet['created_at']),
            "status_id": tweet['id'],
        }

        twitter_id = tweet['user']['id']

        if twitter_id in twitter_ids:
            account = Account.objects.get(twitter_id=twitter_id)
        else:
            account = None

        values['account'] = account

        return cls.objects.create(**values)
