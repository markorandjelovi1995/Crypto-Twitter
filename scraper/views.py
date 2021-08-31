from django.shortcuts import render
from .models import ImportantPerson, NewAccount, ImportantTweet
import os


# Create your views here.

def index(request):
    important_person_rows = ImportantPerson.objects.all()
    new_account_rows = NewAccount.objects.all()
    important_tweet_rows = ImportantTweet.objects.all()
    important_person_all_data = []
    important_tweet_all_data = []
    new_vip_all_data = []

    for row in important_person_rows:
        important_person_all_data.append({"id": row[0], "screen_name": row[1],
                                          "vip_point": row[2], "website": row[3],
                                          "timestamp": row[4]})

    for row in new_account_rows:
        new_vip_all_data.append({"id": row[0], "screen_name": row[1],
                                 "follower_count": row[2], "account_age": row[3], "website": row[4],
                                 "timestamp": row[5]})

    for row in important_tweet_rows:
        important_tweet_all_data.append({"id": row[0], "screen_name": row[1],
                                         "vip_point": row[2], "tweet": row[3],
                                         "timestamp": row[4]})

    return render(request, os.path.join("scraper", "Dashmin_Dark", "Dashmin_html", "index.html"),
                  {"important_person_all_data": important_person_all_data,
                   "important_tweet_all_data": important_tweet_all_data,
                   "new_vip_all_data": new_vip_all_data})
