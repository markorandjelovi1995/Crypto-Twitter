from typing import Any, List, Optional
import tweepy
from constants import TwitterCredential


def get_api_object(cred: TwitterCredential) -> tweepy.API:
    auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
    auth.set_access_token(cred.access_token, cred.access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def get_user_statuses(
    api: tweepy.API, screen_name: str, count: Optional[int] = None, **kwargs: Any
) -> List[tweepy.Status]:
    statuses = []
    if count:
        for status in tweepy.Cursor(
            api.user_timeline, screen_name=screen_name, **kwargs
        ).items(count):
            statuses.append(status)
    else:
        for status in tweepy.Cursor(
            api.user_timeline, screen_name=screen_name, **kwargs
        ).items():
            statuses.append(status)
    return statuses


def get_multiple_user_statuses(
    api: tweepy.API,
    screen_names: List[str],
    count: Optional[int] = None,
    is_verbose: bool = False,
    **kwargs: Any,
) -> List[tweepy.Status]:
    statuses = []
    for i, screen_name in enumerate(screen_names, start=1):
        if is_verbose:
            print(f"{i}/{len(screen_names)}: Getting statuses for {screen_name=}")
        statuses.extend(get_user_statuses(api, screen_name, count, **kwargs))
    return statuses
