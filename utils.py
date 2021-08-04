from typing import Any, List, Optional
import datetime as dt
import json
from pathlib import Path
import click
from constants import TwitterCredential


def read_screen_names(path: Path) -> List[str]:
    with open(path, mode="r") as f:
        raw_data = f.read()
    return raw_data.split("\n")


def read_twitter_credential(path: Path) -> TwitterCredential:
    with open(path, mode="r") as f:
        data = json.load(f)
    cred = TwitterCredential(**data)
    return cred


def parse_isoformat_string(datetime_str: str) -> dt.datetime:
    try:
        datetime_dt = dt.datetime.fromisoformat(datetime_str)
    except Exception:
        raise click.BadParameter("input string must be in ISO format")
    return datetime_dt


def parse_optional_isoformat_string(
    datetime_str: Optional[str],
) -> Optional[dt.datetime]:
    if datetime_str is None:
        return None

    return parse_isoformat_string(datetime_str)
