import re
from django.test import TestCase
from carson.models import Account

class TwitterUtilsTestCase(TestCase):
    def test_write_update(self):
        from carson.utils import write_update
        from cStringIO import StringIO
        from datetime import datetime

        buf = StringIO()
        write_update("foo", buf)
        buf.seek(0)
        self.assertTrue(re.search(r"\033\[2Kfoo (.+)\r", buf.read()))

        buf = StringIO()
        write_update("foo", buf, newline=True)
        buf.seek(0)
        self.assertTrue("\n" in buf.read())

    def test_parse_created_at(self):
        import pytz
        from datetime import datetime
        from carson.utils import parse_created_at

        self.assertEqual(
            parse_created_at("Wed May 23 06:01:13 +0000 2007"),
            datetime(2007, 5, 23, 6, 1, 13, tzinfo=pytz.utc))

        self.assertRaises(AssertionError,
                          parse_created_at, "Wed May 23 06:01:13 -7000 2007")


class TwitterAccountTestCase(TestCase):
    def test_lookup_twitter_ids(self):
        from carson.utils import lookup_twitter_ids

        a = Account.objects.create(twitter_username="TweetNevada")

        ret = lookup_twitter_ids(Account.objects.all())
        self.assertEqual(ret, 1)

        a = Account.objects.get(twitter_username="TweetNevada")
        self.assertEqual(a.twitter_id, 160697962)
