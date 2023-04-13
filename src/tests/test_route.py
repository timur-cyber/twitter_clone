import io
import os

import pytest
import requests as requests
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from src.models import Follow, Like, Media, Tweet, User
from src.utils import followed, liked


def test_add_tweet(
    client: FlaskClient, mock_user: User, _session: Session, mock_headers: dict
) -> None:
    """
    Тест для проверки добавления твита
    :param client: FlaskClient
    :param mock_user: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    request_json = {"tweet_data": "Hello World"}
    resp = client.post("/api/tweets/", json=request_json, headers=mock_headers)
    json_resp = resp.get_json()
    tweet = _session.query(Tweet).get(json_resp.get("tweet_id"))
    assert resp.status_code == 200
    assert resp.json == {"result": True, "tweet_id": tweet.id}
    assert tweet.text == request_json.get("tweet_data")

    _session.delete(tweet)
    _session.commit()


def test_add_media(
    client: FlaskClient, mock_user: User, _session: Session, mock_headers: dict
) -> None:
    """
    Тест для проверки добавления медиа файлов
    :param client: FlaskClient
    :param mock_user: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    URL = "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"
    response = requests.get(URL)
    filename = "test.svg"
    data = {"file": (io.BytesIO(response.content), filename)}
    resp = client.post(
        "/api/medias/",
        data=data,
        content_type="multipart/form-data",
        headers=mock_headers,
    )
    json_resp = resp.get_json()
    media = _session.query(Media).filter(Media.link == f"media/{filename}").one()
    assert resp.status_code == 200
    assert json_resp == {"result": True, "media_id": media.id}
    assert _session.query(Media).get(json_resp.get("media_id"))
    assert os.path.exists(f"media/{filename}")

    _session.delete(media)
    _session.commit()
    os.remove(f"media/{filename}")


def test_delete_tweet(
    client: FlaskClient, mock_user: User, _session: Session, mock_headers: dict
) -> None:
    """
    Тест для проверки удаления твитов
    :param client: FlaskClient
    :param mock_user: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    new_tweet = Tweet(text="Hello World", user_id=mock_user.id)
    _session.add(new_tweet)
    _session.commit()

    resp = client.delete(f"/api/tweets/{new_tweet.id}", headers=mock_headers)
    assert resp.status_code == 200
    assert resp.json == {"result": True}
    assert _session.query(Tweet).get(new_tweet.id) is None


def test_add_like(
    client: FlaskClient,
    mock_user: User,
    mock_tweet: Tweet,
    _session: Session,
    mock_headers: dict,
) -> None:
    """
    Тест для проверки добавления лайков к твиту
    :param client: FlaskClient
    :param mock_user: User
    :param mock_tweet: Tweet
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    resp = client.post(f"/api/tweets/{mock_tweet.id}/likes", headers=mock_headers)
    json_resp = resp.get_json()
    like = liked(mock_user.id, mock_tweet.id)
    assert resp.status_code == 200
    assert json_resp == {"result": True}
    assert like

    _session.delete(like)
    _session.commit()


def test_delete_like(
    client: FlaskClient,
    mock_user: User,
    mock_tweet: Tweet,
    _session: Session,
    mock_headers: dict,
) -> None:
    """
    Тест для проверки удаления лайков к твиту
    :param client: FlaskClient
    :param mock_user: User
    :param mock_tweet: Tweet
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    new_like = Like(user_id=mock_user.id, tweet_id=mock_tweet.id)
    _session.add(new_like)
    _session.commit()

    resp = client.delete(f"/api/tweets/{mock_tweet.id}/likes", headers=mock_headers)
    json_resp = resp.get_json()
    like = liked(mock_user.id, mock_tweet.id)
    assert resp.status_code == 200
    assert json_resp == {"result": True}
    assert not like


def test_follow(
    client: FlaskClient,
    mock_user: User,
    mock_user_2: User,
    _session: Session,
    mock_headers: dict,
) -> None:
    """
    Тест для проверки добавления подписок
    :param client: FlaskClient
    :param mock_user: User
    :param mock_user_2: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    resp = client.post(f"/api/users/{mock_user_2.id}/follow", headers=mock_headers)
    json_resp = resp.get_json()
    follow = followed(mock_user.id, mock_user_2.id)
    assert resp.status_code == 200
    assert json_resp == {"result": True}
    assert follow

    _session.delete(follow)
    _session.commit()


def test_unfollow(
    client: FlaskClient,
    mock_user: User,
    mock_user_2: User,
    _session: Session,
    mock_headers: dict,
) -> None:
    """
    Тест для проверки удаления подписок
    :param client: FlaskClient
    :param mock_user: User
    :param mock_user_2: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    new_follow = Follow(following_user_id=mock_user.id, followed_user_id=mock_user_2.id)
    _session.add(new_follow)
    _session.commit()

    resp = client.delete(f"/api/users/{mock_user_2.id}/follow", headers=mock_headers)
    json_resp = resp.get_json()
    follow = followed(mock_user.id, mock_user_2.id)
    assert resp.status_code == 200
    assert json_resp == {"result": True}
    assert not follow


def test_get_tweets(
    client: FlaskClient,
    mock_user: User,
    mock_user_2: User,
    _session: Session,
    mock_headers: dict,
) -> None:
    """
    Тест для проверки корректности отображаемый ленты
    :param client: FlaskClient
    :param mock_user: User
    :param mock_user_2: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    resp = client.get("/api/tweets/", headers=mock_headers)
    json_resp = resp.get_json()
    assert resp.status_code == 200
    assert json_resp == {"result": True, "tweets": []}

    new_tweet = Tweet(text="Hello World", user_id=mock_user_2.id)
    _session.add(new_tweet)
    _session.commit()
    new_follow = Follow(following_user_id=mock_user.id, followed_user_id=mock_user_2.id)
    _session.add(new_follow)
    _session.commit()
    new_like = Like(user_id=mock_user.id, tweet_id=new_tweet.id)
    _session.add(new_like)
    _session.commit()
    expected_json = {
        "result": True,
        "tweets": [
            {
                "id": new_tweet.id,
                "content": new_tweet.text,
                "attachments": [],
                "author": {"id": mock_user_2.id, "name": mock_user_2.name},
                "likes": [{"user_id": mock_user.id, "name": mock_user.name}],
            }
        ],
    }
    resp = client.get("/api/tweets/", headers=mock_headers)
    json_resp = resp.get_json()
    assert resp.status_code == 200
    assert json_resp == expected_json

    _session.delete(new_tweet)
    _session.delete(new_follow)
    _session.delete(new_like)
    _session.commit()


def test_get_profile_me(
    client: FlaskClient,
    mock_user: User,
    mock_user_2: User,
    _session: Session,
    mock_headers: dict,
) -> None:
    """
    Тест для проверки корректности отображения своего профиля
    :param client: FlaskClient
    :param mock_user: User
    :param mock_user_2: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    resp = client.get("/api/users/me", headers=mock_headers)
    json_resp = resp.get_json()
    assert resp.status_code == 200
    assert json_resp == {
        "result": True,
        "user": {
            "id": mock_user.id,
            "name": mock_user.name,
            "followers": [],
            "following": [],
        },
    }

    follow1 = Follow(following_user_id=mock_user.id, followed_user_id=mock_user_2.id)
    follow2 = Follow(following_user_id=mock_user_2.id, followed_user_id=mock_user.id)
    _session.add(follow1)
    _session.add(follow2)
    _session.commit()
    expected_json = {
        "result": True,
        "user": {
            "id": mock_user.id,
            "name": mock_user.name,
            "followers": [{"id": mock_user_2.id, "name": mock_user_2.name}],
            "following": [{"id": mock_user_2.id, "name": mock_user_2.name}],
        },
    }
    resp = client.get("/api/users/me", headers=mock_headers)
    json_resp = resp.get_json()
    assert resp.status_code == 200
    assert json_resp == expected_json

    _session.delete(follow1)
    _session.delete(follow2)
    _session.commit()


def test_get_profile(
    client: FlaskClient,
    mock_user: User,
    mock_user_2: User,
    _session: Session,
    mock_headers: dict,
) -> None:
    """
    Тест для проверки корректности отображения выбранного профиля
    :param client: FlaskClient
    :param mock_user: User
    :param mock_user_2: User
    :param _session: Session
    :param mock_headers: dict
    :return: None
    """
    resp = client.get(f"/api/users/{mock_user_2.id}", headers=mock_headers)
    json_resp = resp.get_json()
    assert resp.status_code == 200
    assert json_resp == {
        "result": True,
        "user": {
            "id": mock_user_2.id,
            "name": mock_user_2.name,
            "followers": [],
            "following": [],
        },
    }

    follow1 = Follow(following_user_id=mock_user.id, followed_user_id=mock_user_2.id)
    follow2 = Follow(following_user_id=mock_user_2.id, followed_user_id=mock_user.id)
    _session.add(follow1)
    _session.add(follow2)
    _session.commit()
    expected_json = {
        "result": True,
        "user": {
            "id": mock_user_2.id,
            "name": mock_user_2.name,
            "followers": [{"id": mock_user.id, "name": mock_user.name}],
            "following": [{"id": mock_user.id, "name": mock_user.name}],
        },
    }
    resp = client.get(f"/api/users/{mock_user_2.id}", headers=mock_headers)
    json_resp = resp.get_json()
    assert resp.status_code == 200
    assert json_resp == expected_json

    _session.delete(follow1)
    _session.delete(follow2)
    _session.commit()
