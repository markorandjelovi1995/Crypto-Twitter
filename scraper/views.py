from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
import os


# Create your views here.

def index(request):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM Important_Person")
    rows = cursor.fetchall()
    cursor = conn.execute("SELECT * FROM New_Account")
    rows2 = cursor.fetchall()
    cursor = conn.execute("SELECT * FROM Important_Tweet")
    rows3 = cursor.fetchall()
    important_person_all_data = []
    important_tweet_all_data = []
    new_vip_all_data = []

    for row in rows:
        important_person_all_data.append({"id": row[0], "screen_name": row[1],
                         "vip_point": row[2], "website": row[3],
                         "timestamp": row[4]})

    for row in rows2:
        new_vip_all_data.append({"id": row[0], "screen_name": row[1],
                         "follower_count": row[2], "account_age":  row[3], "website": row[4],
                         "timestamp": row[5]})

    for row in rows3:
        important_tweet_all_data.append({"id": row[0], "screen_name": row[1],
                         "vip_point": row[2], "tweet": row[3],
                         "timestamp": row[4]})

    return render(request, os.path.join("scraper", "Dashmin_Dark", "Dashmin_html", "index.html"),
                  {"important_person_all_data": important_person_all_data,
                   "important_tweet_all_data": important_tweet_all_data,
                   "new_vip_all_data": new_vip_all_data})
