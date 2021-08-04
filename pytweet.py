import tweepy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from datetime import datetime, timedelta
from time import sleep
import re
import numpy as np
from pathlib import Path

# auth = tweepy.OAuthHandler("", "")
# auth.set_access_token("",
#                       "")
auth = tweepy.OAuthHandler("M2Jgsi7GWeyXJ3igJWJp529VV", "WOAKOwzhlYf7fCZFKQI4UVv7ZYUHhKRpmysskwILWs07VXx0za")
auth.set_access_token("1400380598942830592-nUNiTzCcdNc4KaOvAMsTPYNnv8BT7T",
                      "eRBPFunnc6a3TYQhJEYiyfQJaEoeGqaiXWs0TMTyCaYKt")
api = tweepy.API(auth)


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
    scraper = webdriver.Chrome(options=options, executable_path='./chromedriver')

    scraper.get("https://www.twitter.com/login")
    sleep(5)
    scraper.find_element_by_name("session[username_or_email]").send_keys("")
    scraper.find_element_by_name("session[password]").send_keys("")
    sleep(5)
    for tweet_id in tweet_ids:
        scraper.get(f"https://www.twitter.com/{screen_name}/status/{tweet_id}")
        sleep(5)

        scraper.get(f"{scraper.current_url}/likes")
        sleep(5)

        get_screen_name = screen_name_regex.findall(scraper.page_source)

        for font in range(0, get_screen_name.count("@font")):
            get_screen_name.remove("@font")
        for font in range(0, get_screen_name.count("@The")):
            get_screen_name.remove("@The")
        for font in range(0, get_screen_name.count("@2x")):
            get_screen_name.remove("@2x")

        print(np.unique(get_screen_name))

    sleep(6000)


def get_follower_info():
    for i in api.followers("DCLBlogger"):
        print(i.screen_name)
        user = api.get_user(i.screen_name)
        print(f"Follwer count: {user.followers_count}")


def get_user_all_follower_info(screen_name):
    for follower in api.followers(screen_name):
        follower_screen_name = follower.screen_name
        follower_info = api.get_user(follower_screen_name)
        print(f"Follower Name: {follower_info.name}")
        print(f"Follower Screen Name: {follower_screen_name}")
        print(f"Follower Account Age : {follower_info.created_at}")
        print(f"Follower Followers Count : {follower_info.followers_count}")
        print(f"Follower Following Count : {follower_info.friends_count}")
        print("\n\n")


if __name__ == "__main__":
    screen_name_list = Path("test_screen_name.txt").read_text().split()
    for screen_name in screen_name_list:
        get_user_all_follower_info(screen_name)
        get_tweet(screen_name)

    print("Done")
