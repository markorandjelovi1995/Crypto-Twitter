from django.db import models


# Create your models here.

class ImportantPerson(models.Model):
    screen_name = models.CharField(max_length=999)
    vip_point = models.IntegerField()
    website_url = models.CharField(max_length=999, null=True)
    timestamp = models.CharField(max_length=999)

    class Meta:
        db_table = f'"{__package__}_important_person"'


class NewAccount(models.Model):
    screen_name = models.CharField(max_length=999)
    follower_count = models.IntegerField()
    account_creation_date = models.CharField(max_length=999)
    website_url = models.CharField(max_length=999, null=True)
    timestamp = models.CharField(max_length=999)

    class Meta:
        db_table = f'"{__package__}_new_account"'


class ImportantTweet(models.Model):
    screen_name = models.CharField(max_length=999)
    vip_point = models.IntegerField()
    tweet = models.CharField(max_length=999)
    timestamp = models.CharField(max_length=999)

    class Meta:
        db_table = f'"{__package__}_important_tweet"'

