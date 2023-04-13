from typing import Union

from sqlalchemy import and_, exc

from src.models import Follow, Like, Media, Tweet, User, session


def show_tweets(user_id: int) -> dict:
    """
    Функция для отобраджения информации твитов в ленте по user_id
    :param user_id: int
    :return: dict
    """
    followings = session.query(Follow).filter(Follow.following_user_id == user_id).all()
    tweets_respond = list()
    tweets = list()
    my_tweets = session.query(Tweet).filter(Tweet.user_id == user_id).all()
    tweets.extend(my_tweets)
    if followings:
        for follow in followings:
            user_tweets = (
                session.query(Tweet)
                .filter(Tweet.user_id == follow.followed_user_id)
                .all()
            )
            tweets.extend(user_tweets)
    tweets = sorted(tweets, key=lambda x: x.datetime, reverse=True)
    for tweet in tweets:
        media_obj = list()
        likes = list()
        if tweet.media:
            for media_id in tweet.media:
                media_obj.append(session.query(Media).get(media_id))
        else:
            media_obj = []
        like_query = session.query(Like).filter(Like.tweet_id == tweet.id).all()
        if like_query:
            for like in like_query:
                likes.append(
                    {
                        "user_id": like.user_id,
                        "name": session.query(User).get(like.user_id).name,
                    }
                )
        else:
            likes = []
        resp = {
            "id": tweet.id,
            "content": tweet.text,
            "attachments": [
                media.link if media is not None else None for media in media_obj
            ],
            "author": {
                "id": tweet.user_id,
                "name": session.query(User).get(tweet.user_id).name,
            },
            "likes": likes,
        }
        tweets_respond.append(resp)

    response = {"result": True, "tweets": tweets_respond}
    return response


def show_profile(user_id: int) -> dict:
    """
    Функция для отобраджения информации профиля по user_id
    :param user_id: int
    :return: dict
    """
    user = session.query(User).filter(User.id == user_id).first()
    followers_query = [
        a.following_user_id
        for a in session.query(Follow).filter(Follow.followed_user_id == user_id).all()
    ]
    followed_query = [
        a.followed_user_id
        for a in session.query(Follow).filter(Follow.following_user_id == user_id).all()
    ]
    if followers_query:
        followers = list()
        for follower_id in followers_query:
            follower_user = session.query(User).get(follower_id)
            followers.append({"id": follower_user.id, "name": follower_user.name})
    else:
        followers = []
    if followed_query:
        followed = list()
        for followed_id in followed_query:
            followed_user = session.query(User).get(followed_id)
            followed.append({"id": followed_user.id, "name": followed_user.name})
    else:
        followed = []
    response = {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": followers,
            "following": followed,
        },
    }
    return response


def followed(following_id: int, followed_id: int) -> Union[Follow, bool]:
    """
    Функция для отображения объекта Follow, если он не найден возвращает False
    :param following_id: int
    :param followed_id: int
    :return: Follow | bool
    """
    try:
        return (
            session.query(Follow)
            .filter(
                and_(
                    Follow.following_user_id == following_id,
                    Follow.followed_user_id == followed_id,
                )
            )
            .one()
        )
    except exc.NoResultFound:
        return False


def liked(user_id, tweet_id) -> Union[Like, bool]:
    """
    Функция для отображения объекта Like, если он не найден возвращает False
    :param user_id: int
    :param tweet_id: int
    :return: Like | bool
    """
    try:
        return (
            session.query(Like)
            .filter(and_(Like.user_id == user_id, Like.tweet_id == tweet_id))
            .one()
        )
    except exc.NoResultFound:
        return False
