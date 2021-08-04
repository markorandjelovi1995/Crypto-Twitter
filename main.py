from typing import Optional
import datetime as dt
from pathlib import Path
import click
import dotenv
from db import (
    get_daily_statuses,
    get_db_object,
    get_monthly_statuses,
    get_statuses_from_db,
    get_weekly_statuses,
    insert_statuses_to_db,
)
from fetch import (
    get_api_object,
    get_multiple_user_statuses,
)
from status import (
    get_top_statuses,
    statuses_with_score_to_str,
    status_to_dict,
)
from utils import (
    parse_optional_isoformat_string,
    read_screen_names,
    read_twitter_credential,
)


@click.group()
def cli():
    dotenv.load_dotenv()


@cli.command()
@click.option(
    "-s",
    "--screen-names",
    "screen_names_txt_path",
    envvar="SCREEN_NAMES_TXT_PATH",
    show_envvar=True,
    type=click.Path(exists=True),
    help="path to txt file containing screen names (single screen name in each line)",
    required=True,
)
@click.option(
    "-c",
    "--credential",
    "twitter_credential_path",
    envvar="TWITTER_CREDENTIAL_PATH",
    show_envvar=True,
    type=click.Path(exists=True),
    help="path to json file containing twitter api credentials (must contain consumer_key, consumer_secret, access_token and access_token_secret fields)",
    required=True,
)
@click.option(
    "-d",
    "--db",
    "db_path",
    envvar="DB_PATH",
    show_envvar=True,
    type=click.Path(),
    help="path to database json file (for tinydb json storage)",
    required=True,
)
@click.option(
    "--count",
    default=200,
    show_default=True,
    type=int,
    help="maximum number of statuses to fetch for each screen name (1 request per 200 statuses per user)",
)
@click.option(
    "-v",
    "--verbose",
    default=False,
    show_default=True,
    type=bool,
    help="verbosity",
)
def fetch(
    screen_names_txt_path: str,
    twitter_credential_path: str,
    db_path: str,
    count: int,
    verbose: bool,
) -> None:
    cred = read_twitter_credential(Path(twitter_credential_path))
    api = get_api_object(cred)
    db = get_db_object(Path(db_path))
    screen_names = read_screen_names(Path(screen_names_txt_path))

    statuses = get_multiple_user_statuses(
        api,
        screen_names=screen_names,
        count=count,
        is_verbose=verbose,
        trim_user=False,
        exclude_replies=False,
        include_rts=True,
        tweet_mode="extended",
    )
    status_objects = list(map(status_to_dict, statuses))
    insert_statuses_to_db(db, status_objects)


@cli.command()
@click.option(
    "-d",
    "--db",
    "db_path",
    envvar="DB_PATH",
    show_envvar=True,
    type=click.Path(exists=True),
    help="path to database json file (for tinydb json storage)",
    required=True,
)
@click.option(
    "-c",
    "--count",
    default=5,
    show_default=True,
    type=int,
    help="returns (at most) top `count` statuses",
)
@click.option(
    "--date",
    default=str(dt.date.today()),
    show_default="today",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="filter statuses on `date` (in ISO format)",
)
@click.option(
    "--tweet/--no-tweet",
    default=None,
    show_default=True,
    help="include only tweets / exclude tweets",
)
@click.option(
    "--reply/--no-reply",
    default=None,
    show_default=True,
    help="include only replies / exclude replies",
)
@click.option(
    "--retweet/--no-retweet",
    default=None,
    show_default=True,
    help="include only retweets / exclude retweets",
)
@click.option(
    "--quote/--no-quote",
    default=None,
    show_default=True,
    help="include only quotes / exclude quotes",
)
def daily(
    db_path: str,
    count: int,
    date: dt.datetime,
    tweet: Optional[bool],
    reply: Optional[bool],
    retweet: Optional[bool],
    quote: Optional[bool],
) -> None:
    db = get_db_object(Path(db_path))
    statuses = get_daily_statuses(db, date, tweet, reply, retweet, quote)
    top_statuses_with_score = get_top_statuses(statuses, count)
    result_str = statuses_with_score_to_str(top_statuses_with_score)
    date_str = date.date().isoformat()
    print(f"Important statuses on {date_str}")
    print("----------")
    print(result_str)


@cli.command()
@click.option(
    "-d",
    "--db",
    "db_path",
    envvar="DB_PATH",
    show_envvar=True,
    type=click.Path(exists=True),
    help="path to database json file (for tinydb json storage)",
    required=True,
)
@click.option(
    "-c",
    "--count",
    default=5,
    show_default=True,
    type=int,
    help="returns (at most) top `count` statuses",
)
@click.option(
    "--date",
    default=str(dt.date.today()),
    show_default="today",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="filter statuses in week containing `date` (in ISO format)",
)
@click.option(
    "--tweet/--no-tweet",
    default=None,
    show_default=True,
    help="include only tweets / exclude tweets",
)
@click.option(
    "--reply/--no-reply",
    default=None,
    show_default=True,
    help="include only replies / exclude replies",
)
@click.option(
    "--retweet/--no-retweet",
    default=None,
    show_default=True,
    help="include only retweets / exclude retweets",
)
@click.option(
    "--quote/--no-quote",
    default=None,
    show_default=True,
    help="include only quotes / exclude quotes",
)
def weekly(
    db_path: str,
    count: int,
    date: dt.datetime,
    tweet: Optional[bool],
    reply: Optional[bool],
    retweet: Optional[bool],
    quote: Optional[bool],
) -> None:
    since = date - dt.timedelta(days=date.weekday())
    since = dt.datetime(since.year, since.month, since.day)
    until = since + dt.timedelta(days=7)
    db = get_db_object(Path(db_path))
    statuses = get_weekly_statuses(db, date, tweet, reply, retweet, quote)
    top_statuses_with_score = get_top_statuses(statuses, count)
    result_str = statuses_with_score_to_str(top_statuses_with_score)
    since_str = since.date().isoformat()
    until_str = until.date().isoformat()

    print(f"Important statuses in week {since_str} - {until_str}")
    print("----------")
    print(result_str)


@cli.command()
@click.option(
    "-d",
    "--db",
    "db_path",
    envvar="DB_PATH",
    show_envvar=True,
    type=click.Path(exists=True),
    help="path to database json file (for tinydb json storage)",
    required=True,
)
@click.option(
    "-c",
    "--count",
    default=5,
    show_default=True,
    type=int,
    help="returns (at most) top `count` statuses",
)
@click.option(
    "--date",
    default=str(dt.date.today()),
    show_default="today",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="filter statuses in month containing `date` (in ISO format)",
)
@click.option(
    "--tweet/--no-tweet",
    default=None,
    show_default=True,
    help="include only tweets / exclude tweets",
)
@click.option(
    "--reply/--no-reply",
    default=None,
    show_default=True,
    help="include only replies / exclude replies",
)
@click.option(
    "--retweet/--no-retweet",
    default=None,
    show_default=True,
    help="include only retweets / exclude retweets",
)
@click.option(
    "--quote/--no-quote",
    default=None,
    show_default=True,
    help="include only quotes / exclude quotes",
)
def monthly(
    db_path: str,
    count: int,
    date: dt.datetime,
    tweet: Optional[bool],
    reply: Optional[bool],
    retweet: Optional[bool],
    quote: Optional[bool],
) -> None:
    since = dt.datetime(date.year, date.month, 1)
    until = (since + dt.timedelta(days=32)).replace(day=1)
    db = get_db_object(Path(db_path))
    statuses = get_monthly_statuses(db, date, tweet, reply, retweet, quote)
    top_statuses_with_score = get_top_statuses(statuses, count)
    result_str = statuses_with_score_to_str(top_statuses_with_score)
    since_str = since.date().isoformat()
    until_str = until.date().isoformat()

    print(f"Important statuses in month {since_str} - {until_str}")
    print("----------")
    print(result_str)


@cli.command()
@click.option(
    "-d",
    "--db",
    "db_path",
    envvar="DB_PATH",
    show_envvar=True,
    type=click.Path(exists=True),
    help="path to database json file (for tinydb json storage)",
    required=True,
)
@click.option(
    "-c",
    "--count",
    default=5,
    show_default=True,
    type=int,
    help="returns (at most) top `count` statuses",
)
@click.option(
    "--since",
    default=None,
    show_default=True,
    type=parse_optional_isoformat_string,
    metavar="Optional[%Y-%m-%d]",
    help="filter statuses since datetime (in ISO format)",
)
@click.option(
    "--until",
    default=None,
    show_default=True,
    type=parse_optional_isoformat_string,
    metavar="Optional[%Y-%m-%d]",
    help="filter statuses until datetime (in ISO format)",
)
@click.option(
    "--tweet/--no-tweet",
    default=None,
    show_default=True,
    help="include only tweets / exclude tweets",
)
@click.option(
    "--reply/--no-reply",
    default=None,
    show_default=True,
    help="include only replies / exclude replies",
)
@click.option(
    "--retweet/--no-retweet",
    default=None,
    show_default=True,
    help="include only retweets / exclude retweets",
)
@click.option(
    "--quote/--no-quote",
    default=None,
    show_default=True,
    help="include only quotes / exclude quotes",
)
def historical(
    db_path: str,
    count: int,
    since: Optional[dt.datetime],
    until: Optional[dt.datetime],
    tweet: Optional[bool],
    reply: Optional[bool],
    retweet: Optional[bool],
    quote: Optional[bool],
) -> None:
    db = get_db_object(Path(db_path))
    statuses = get_statuses_from_db(db, since, until, tweet, reply, retweet, quote)
    top_statuses_with_score = get_top_statuses(statuses, count)
    result_str = statuses_with_score_to_str(top_statuses_with_score)
    since_str = since.isoformat() if since else "x"
    until_str = until.isoformat() if until else "x"
    print(f"Important statuses between {since_str} - {until_str}")
    print("----------")
    print(result_str)


if __name__ == "__main__":
    cli()
