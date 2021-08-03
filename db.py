from typing import List, Optional, Tuple, Union
import datetime as dt
from pathlib import Path
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from constants import StatusAsDict


def get_db_object(path: Path) -> TinyDB:
    serialization = SerializationMiddleware(JSONStorage)
    serialization.register_serializer(DateTimeSerializer(), "DateTimeSerializer")
    db = TinyDB(path, storage=serialization)
    return db


def insert_statuses_to_db(db: TinyDB, statuses: List[StatusAsDict]) -> None:
    db.insert_multiple(statuses)


def get_statuses_from_db(
    db: TinyDB,
    since: Optional[dt.datetime] = None,
    until: Optional[dt.datetime] = None,
    is_tweet: Optional[bool] = None,
    is_reply: Optional[bool] = None,
    is_retweet: Optional[bool] = None,
    is_quote: Optional[bool] = None,
) -> List[StatusAsDict]:
    query = Query()
    query_since = query.metadata.created_at >= since if since else query.noop()
    query_until = query.metadata.created_at <= until if until else query.noop()
    query_date = query_since & query_until

    query_tweet = (
        query.features.is_tweet == is_tweet if is_tweet is not None else query.noop()
    )
    query_reply = (
        query.features.is_reply == is_reply if is_reply is not None else query.noop()
    )
    query_retweet = (
        query.features.is_retweet == is_retweet
        if is_retweet is not None
        else query.noop()
    )
    query_quote = (
        query.features.is_quote == is_quote if is_quote is not None else query.noop()
    )
    query_status_type = query_tweet & query_reply & query_retweet & query_quote

    query_combined = query_date & query_status_type
    return db.search(query_combined)


def get_daily_statuses(
    db: TinyDB,
    date: Union[dt.date, dt.datetime],
    is_tweet: Optional[bool] = None,
    is_reply: Optional[bool] = None,
    is_retweet: Optional[bool] = None,
    is_quote: Optional[bool] = None,
) -> List[StatusAsDict]:
    since = dt.datetime(date.year, date.month, date.day)
    until = since + dt.timedelta(days=1)
    statuses = get_statuses_from_db(
        db, since, until, is_tweet, is_reply, is_retweet, is_quote
    )
    return statuses


def get_weekly_statuses(
    db: TinyDB,
    date: Union[dt.date, dt.datetime],
    is_tweet: Optional[bool] = None,
    is_reply: Optional[bool] = None,
    is_retweet: Optional[bool] = None,
    is_quote: Optional[bool] = None,
) -> List[StatusAsDict]:
    since = date - dt.timedelta(days=date.weekday())
    since = dt.datetime(since.year, since.month, since.day)
    until = since + dt.timedelta(days=7)
    statuses = get_statuses_from_db(
        db, since, until, is_tweet, is_reply, is_retweet, is_quote
    )
    return statuses


def get_monthly_statuses(
    db: TinyDB,
    date: Union[dt.date, dt.datetime],
    is_tweet: Optional[bool] = None,
    is_reply: Optional[bool] = None,
    is_retweet: Optional[bool] = None,
    is_quote: Optional[bool] = None,
) -> List[StatusAsDict]:
    since = dt.datetime(date.year, date.month, 1)
    until = (since + dt.timedelta(days=32)).replace(day=1)
    statuses = get_statuses_from_db(
        db, since, until, is_tweet, is_reply, is_retweet, is_quote
    )
    return statuses
