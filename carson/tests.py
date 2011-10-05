from django.test import TestCase
from carson.models import Account

class TwitterAccountTestCase(TestCase):
    def test_lookup_twitter_ids(self):
        from carson.utils import lookup_twitter_ids

        a = Account.objects.create(twitter_username="TweetNevada")

        ret = lookup_twitter_ids(Account.objects.all())
        self.assertEqual(ret, 1)

        a = Account.objects.get(twitter_username="TweetNevada")
        self.assertEqual(a.twitter_id, 160697962)
