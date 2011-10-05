from django.test import TestCase
from carson.models import Account

class TwitterUtilsTestCase(TestCase):
    def test_write_update(self):
        from carson.utils import write_update
        from cStringIO import StringIO

        buf = StringIO()
        write_update("foo", buf)
        buf.seek(0)
        self.assertEqual(buf.read(), "\033[2Kfoo\r")

        buf.seek(0)
        write_update("foo", buf, newline=True)
        buf.seek(0)
        self.assertEqual(buf.read(), "\033[2Kfoo\n")


class TwitterAccountTestCase(TestCase):
    def test_lookup_twitter_ids(self):
        from carson.utils import lookup_twitter_ids

        a = Account.objects.create(twitter_username="TweetNevada")

        ret = lookup_twitter_ids(Account.objects.all())
        self.assertEqual(ret, 1)

        a = Account.objects.get(twitter_username="TweetNevada")
        self.assertEqual(a.twitter_id, 160697962)
