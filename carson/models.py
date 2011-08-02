import sys
import json
from django.db import models
from carson.utils import parse_created_at
from carson.managers import TrustedManager, UntrustedManager

class Account(models.Model):
    twitter_username = models.CharField(max_length=32)
    twitter_id = models.PositiveIntegerField()

    def __unicode__(self):
        return u"@%s" % self.twitter_username

class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return self.name

class Tweet(models.Model):
    account = models.ForeignKey(Account, null=True, related_name="tweets")
    tweet_id = models.BigIntegerField()
    timestamp = models.DateTimeField()
    text = models.TextField()

    objects = models.Manager()
    trusted = TrustedManager()
    untrusted = UntrustedManager()

    def __unicode__(self):
        return unicode(self.tweet_id)

    @classmethod
    def add(cls, tweet):
        # Only load if passed a string
        if isinstance(tweet, basestring):
            tweet = json.loads(tweet)

        values = {
            "tweet_id"  : tweet['id'],
            "timestamp" : parse_created_at(tweet['created_at']),
            "text"      : tweet['text'],
        }

        # If the tweet came from a whitelisted Account, include it
        try:
            account = Account.objects.get(twitter_id=tweet['user']['id'])
        except Account.DoesNotExist:
            account = None

        values['account'] = account

        sys.stdout.write("Added %d\r" % tweet['id'])
        sys.stdout.flush()

        return cls.objects.create(**values)
