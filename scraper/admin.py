from django.contrib import admin
from .models import ImportantPerson, NewAccount, ImportantTweet


# Register your models here.

class ImportantPersonAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "vip_point", "website_url", "timestamp")


class NewAccountAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "follower_count", "account_creation_date", "website_url", "timestamp")


class ImportantTweetAdmin(admin.ModelAdmin):
    list_display = ("screen_name", "vip_point", "tweet", "timestamp")


admin.site.register(ImportantPerson, ImportantPersonAdmin)
admin.site.register(NewAccount, NewAccountAdmin)
admin.site.register(ImportantTweet, ImportantTweetAdmin)
