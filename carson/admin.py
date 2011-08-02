from django.contrib import admin
from carson.models import Account, Tag
from carson.utils import lookup_twitter_ids

class AccountAdmin(admin.ModelAdmin):
    list_display = ["twitter_username", "twitter_id"]
    actions = ['populate_twitter_ids']

    def populate_twitter_ids(self, request, queryset):
        updated = lookup_twitter_ids(queryset)
        self.message_user(request, "%d account(s) updated" % updated)
    populate_twitter_ids.short_description = "Lookup Twitter IDs"

admin.site.register(Account, AccountAdmin)
admin.site.register(Tag)
