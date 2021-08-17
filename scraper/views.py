from django.shortcuts import render
from django.http import HttpResponse
import sqlite3


# Create your views here.

def index(request):
    # x = [{'name': 'Mr. Shaw', 'office': 'Orange LLP', 'address': '123 Main Str'}, \
    #     {'name': 'Bill', 'office': 'Apple LLP', 'address': '124 Bone St'}]

    # all_data = [{'name': all_data['name'][i], 'office': all_data['office'][i], ...} for i in
    #             range(len(all_data['name']))]

    # return render(request, "scraper\Dashmin_Dark\Dashmin_html\index.html",
    #               {"id_list": id_list, "screen_name_list": screen_name_list,
    #                "vip_point_list": vip_point_list, "website_url_list": website_url_list,
    #                "timestamp_list": timestamp_list})

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

    return render(request, "scraper\Dashmin_Dark\Dashmin_html\index.html",
                  {"important_person_all_data": important_person_all_data,
                   "important_tweet_all_data": important_tweet_all_data,
                   "new_vip_all_data": new_vip_all_data})
    # return HttpResponse("<h1>hi</h1>")
def ajaxdata(request):
    from django.http import JsonResponse
    return JsonResponse({"a":"b"})

def datatable(request):
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM New_Account")
    rows = cursor.fetchall()
    important_person_all_data = []

    for row in rows:
        important_person_all_data.append({"id": row[0], "screen_name": row[1],
                                          "vip_point": row[2], "url": row[3],
                                          "timestamp": row[4]})

    return render(request, "scraper\Dashmin_Dark\Dashmin_html\indextest.html",
                  {"important_person_all_data": important_person_all_data})