import tweepy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from datetime import datetime, timedelta
from time import sleep
import re
import numpy as np
from pathlib import Path
import sqlite3
import json


def get_tweet(screen_name):
    tweets_list = []
    tweet_ids = []
    number_of_recent_post = 100
    historical_tweet_date = datetime.now() - timedelta(14)
    tweets = tweepy.Cursor(api.user_timeline, id=screen_name).items(number_of_recent_post)

    for tweet in tweets:
        if tweet.created_at > historical_tweet_date:
            tweets_list.append([tweet.created_at, tweet.id, tweet.text])
        else:
            break

    pprint(tweets_list)
    for tweet_id in tweets_list:
        tweet_ids.append(tweet_id[1])
    get_favourite(screen_name, tweet_ids)


def get_favourite(screen_name, tweet_ids):
    screen_name_regex = re.compile(r"@[a-zA-Z0-9]+")
    get_screen_name = []
    options = Options()
    options.add_argument("no-sandbox")
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument('--no-proxy-server')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("start-maximized")
    options.add_argument("window-size=1900,1080")
    options.add_argument("--log-level=3")
    try:
        scraper = webdriver.Chrome(options=options, executable_path='chromedriver.exe')
    except:
        scraper = webdriver.Chrome(options=options, executable_path='./chromedriver')
    scraper.get("https://www.twitter.com/login")
    sleep(10)
    scraper.find_element_by_name("session[username_or_email]").send_keys(credentials["username"])
    scraper.find_element_by_name("session[password]").send_keys(credentials["password"] + "\n")
    sleep(15)
    
    for tweet_id in tweet_ids:
        scraper.get(f"https://www.twitter.com/{screen_name}/status/{tweet_id}")
        sleep(15)
        scraper.get(f"{scraper.current_url}/likes")
        sleep(20)
                
        for i in scraper.find_elements_by_class_name("r-14j79pv"):
            if i.get_attribute("dir") == "ltr":
                found_screen_name = screen_name_regex.findall(i.text)
                if found_screen_name:
                    print(i.text)
                    get_screen_name.append(str(found_screen_name[0]).replace("@", ""))

    get_screen_name = np.unique(get_screen_name)
    print(get_screen_name)
    cross_check_screen_name(screen_name_list, get_screen_name, screen_name, "Important_Tweet")
    scraper.quit()


def get_user_all_follower_info(screen_name, screen_name_list):
    friend_screen_name_list = []
    friend_ids = []
    count = 0

    for page in tweepy.Cursor(api.friends_ids, screen_name=screen_name).pages():
        friend_ids.extend(page)

    print(f"{screen_name} following count : {len(friend_ids)}")

    for friend_id in friend_ids:
        try:
            count += 1
            print(f"Profile checked : {count}")
            friend_info = api.get_user(friend_id)
            friend_screen_name_list.append(friend_info.screen_name)
            print(f"Scraping Friend Info of : {screen_name}")
            print(f"Friend Name: {friend_info.name}")
            print(f"Friend Screen Name: {friend_info.screen_name}")
            print(f"Friend Account Age : {friend_info.created_at}")
            print(f"Friend Followers Count : {friend_info.followers_count}")
            print(f"Friend Following Count : {friend_info.friends_count}")
            print("\n")
        except tweepy.TweepError:
            print(f"Failed to get {screen_name} follower info this user has protection enable")
    cross_check_screen_name(screen_name_list, friend_screen_name_list, screen_name, "Important_Person")


def get_new_vip_account(screen_name):
    ids = []
    count = 0
    for page in tweepy.Cursor(api.friends_ids, screen_name=screen_name).pages():
        ids.extend(page)

    print(f"{screen_name} Following count: {len(ids)} ")

    for i in ids:
        user = api.get_user(i)
        count += 1
        print(f"Profile checked : {count}")

        print(user.screen_name)

        if user.followers_count <= 800:
            print(f"New VIP account condition met for {user.screen_name}: {user.followers_count}, {user.created_at}, {user.url}")
            conn = sqlite3.connect('database.db')
            conn.execute(f'''CREATE TABLE IF NOT EXISTS New_Account 
                             (ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
                             Screen_Name           TEXT    NOT NULL,
                             Follower_Count            INTEGER     NOT NULL,
                             Account_Creation_Date TEXT  NOT NULL,
                             Website_URL TEXT,
                             Scraping_Timestamp TEXT NOT NULL);''')
            conn.execute(f"INSERT INTO New_Account (Screen_Name, Follower_count, Account_Creation_Date, Website_URL, Scraping_Timestamp) \
                          VALUES (?,?,?,?,?)", (user.screen_name, user.followers_count, user.created_at, user.url, datetime.now()))
            conn.commit()
            conn.close()


def cross_check_screen_name(screen_name_list, returned_screen_name, influencer_screen_name, table_name):
    vip_point = 0

    for screen_name in returned_screen_name:
        if screen_name in screen_name_list:
            vip_point += 1

    print(f"{influencer_screen_name} VIP POINT is : {vip_point}")

    if vip_point:
        conn = sqlite3.connect('database.db')
        conn.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} 
                 (ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
                 Screen_Name           TEXT    NOT NULL,
                 VIP_Point            INTEGER     NOT NULL,
                 Website_URL  TEXT,
                 Timestamp TEXT NOT NULL);''')
        conn.execute(f"INSERT INTO {table_name} (Screen_Name, VIP_Point, Website_URL,Timestamp) \
              VALUES (?,?,?,?)", (influencer_screen_name, vip_point, api.get_user(influencer_screen_name).url, datetime.now()))
        conn.commit()
        conn.close()

credentials = json.loads(Path("credentials.json").read_text())
auth = tweepy.OAuthHandler(credentials["api_key"], credentials["api_secret"])
auth.set_access_token(credentials["token_access"], credentials["token_secret"])
api = tweepy.API(auth, wait_on_rate_limit=True)

if __name__ == "__main__":
    screen_name_list = Path("test_screen_name.txt").read_text().split()
    while True:
        for screen_name in screen_name_list:
            get_new_vip_account(screen_name)
            get_user_all_follower_info(screen_name, screen_name_list)
            get_tweet(screen_name)
        print("WAITING FOR 1 MIN ")
        sleep(60)

