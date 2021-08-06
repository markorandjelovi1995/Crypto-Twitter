from typing import Any, Dict, List, Literal, Mapping, Tuple
import tweepy
from constants import StatusAsDict


def get_status_type(
    status: tweepy.Status,
) -> Literal["tweet", "reply", "retweet", "quote"]:
    status_json = status._json
    if status_json.get("retweeted_status", None) is not None:
        return "retweet"
    elif status_json["in_reply_to_screen_name"] is not None:
        return "reply"
    elif status_json["is_quote_status"]:
        return "quote"
    else:
        return "tweet"


def status_to_features(status: tweepy.Status) -> Dict[str, float]:
    status_json = status._json
    status_type = get_status_type(status)
    features = {
        "is_reply": status_type == "reply",
        "is_quote": status_type == "quote",
        "is_retweet": status_type == "retweet",
        "is_tweet": status_type == "tweet",
        "favorite_count": status_json["favorite_count"],
        "retweet_count": status_json["retweet_count"],
        "user": {
            "favourites_count": status_json["user"]["favourites_count"],
            "followers_count": status_json["user"]["followers_count"],
            "friends_count": status_json["user"]["friends_count"],
            "listed_count": status_json["user"]["listed_count"],
            "statuses_count": status_json["user"]["statuses_count"],
        },
    }
    return features


def status_to_dict(status: tweepy.Status) -> StatusAsDict:
    metadata = {
        "id_str": status.id_str,
        "created_at": status.created_at,
        "text": status.full_text,
        "user": {
            "id_str": status.user.id_str,
            "screen_name": status.user.screen_name,
        },
    }
    features = status_to_features(status)
    status_dict = {
        "metadata": metadata,
        "features": features,
    }
    return status_dict


def features_to_importance_score(
    features: Mapping[str, float], feature_weights: Mapping[str, float]
) -> float:
    score = sum(
        [
            features.get(feature, 0) * weight
            for feature, weight in feature_weights.items()
        ]
    )
    return score


def status_to_str(status: StatusAsDict, score: float) -> str:
    datetime = status["metadata"]["created_at"]
    screen_name = status["metadata"]["user"]["screen_name"]
    status_id = status["metadata"]["id_str"]
    status_url = f"https://twitter.com/x/status/{status_id}"
    text = status["metadata"]["text"]
    return f"- {score=}\n@{screen_name}\n{datetime}\n{status_url}\n{text}"


def get_top_statuses(
    statuses: List[StatusAsDict],
    count: int,
) -> List[Tuple[float, StatusAsDict]]:
    feature_weights = {
        "favorite_count": 1,
        "retweet_count": 3,
    }
    scores = map(
        lambda s: features_to_importance_score(s["features"], feature_weights), statuses
    )
    scores_and_statuses = sorted(
        zip(scores, statuses), key=lambda x: x[0], reverse=True
    )
    top_k = scores_and_statuses[:count]
    return top_k


def statuses_with_score_to_str(
    statuses_with_score: List[Tuple[float, StatusAsDict]]
) -> str:
    return "\n----------\n".join(
        map(lambda x: status_to_str(x[1], x[0]), statuses_with_score)
    )
