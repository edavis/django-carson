from django.db import models

class TrustedManager(models.Manager):
    def get_query_set(self):
        return super(TrustedManager, self).get_query_set().exclude(account=None)

class UntrustedManager(models.Manager):
    def get_query_set(self):
        return super(UntrustedManager, self).get_query_set().filter(account=None)
