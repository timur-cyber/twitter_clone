import logging
import logging.config
import os

import flask
import sentry_sdk
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger, swag_from
from flask import Flask, jsonify, render_template, request
from flask_injector import FlaskInjector
from flask_restful import Api
from prometheus_flask_exporter import PrometheusMetrics
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from src.depends import UserIdDepend, configure
from src.log_config import dict_config
from src.models import Follow, Like, Media, Tweet, session
from src.schemas import FollowSchema, LikeSchema, MediaSchema, TweetSchema, UserSchema
from src.utils import followed, liked, show_profile, show_tweets

root_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(root_dir, "templates")
js_directory = os.path.join(template_folder, "static/js")
css_directory = os.path.join(template_folder, "static/css")
images_directory = os.path.join(template_folder, "static/images")
static_directory = os.path.join(template_folder, "static")

app = Flask(__name__, template_folder=template_folder)

app.config["UPLOAD_FOLDER"] = "media/"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

api = Api(app)

spec = APISpec(
    title="Tweeter API",
    version="1.0.0",
    openapi_version="2.0",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

template = spec.to_flasgger(
    app, definitions=[UserSchema, TweetSchema, MediaSchema, LikeSchema, FollowSchema]
)

swagger = Swagger(app, template=template)

logging.config.dictConfig(dict_config)
logger = logging.getLogger("twitter log")

sentry_sdk.init(
    dsn=os.environ.get("dsn"),
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0,
)

metrics = PrometheusMetrics(app)


@app.route("/", methods=["GET", "POST"])
def main() -> str:
    """
    Главный endpoint для отображения Front-end части
    :return: str
    """
    return render_template("index.html")


@swag_from("docs/add_tweet.yml")
@app.route("/api/tweets/", methods=["POST"])
def add_tweet(user_id: UserIdDepend) -> flask.wrappers.Response:
    """
    Endpoint для добавления твита
    :return: Response
    """
    data = request.get_json()
    tweet_data = data.get("tweet_data")
    tweet_media_ids = data.get("tweet_media_ids")
    new_tweet = Tweet(user_id=user_id, text=tweet_data, media=tweet_media_ids)
    session.add(new_tweet)
    session.commit()
    response = {"result": True, "tweet_id": new_tweet.id}
    logger.debug(f"User (ID: {user_id}) added Tweet (ID: {new_tweet.id})")
    return jsonify(response)


@swag_from("docs/download_media.yml")
@app.route("/api/medias/", methods=["POST"])
def download_media(user_id: UserIdDepend) -> flask.wrappers.Response:
    """
    Endpoint для добавления медиа файлов
    :return: Response
    """
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    file.close()
    new_media = Media(link=file_path)
    session.add(new_media)
    session.commit()
    response = {"result": True, "media_id": new_media.id}
    logger.debug(f"User (ID: {user_id}) added Media (ID: {new_media.id})")
    return jsonify(response)


@swag_from("docs/delete_tweet.yml")
@app.route("/api/tweets/<id>", methods=["DELETE"])
def delete_tweet(user_id: UserIdDepend, id: int) -> flask.wrappers.Response:
    """
    Endpoint для удаления твитов
    :param id: int
    :return: Response
    """
    tweet = session.query(Tweet).get(id)
    session.delete(tweet)
    session.commit()
    response = {"result": True}
    logger.debug(f"User (ID: {user_id}) deleted Tweet (ID: {tweet.id})")
    return jsonify(response)


@swag_from("docs/put_like.yml")
@app.route("/api/tweets/<id>/likes", methods=["POST"])
def put_like(user_id: UserIdDepend, id: int) -> flask.wrappers.Response:
    """
    Endpoint для добавления лайков
    :param id: int
    :return: Response
    """
    if not liked(user_id, id):
        new_like = Like(user_id=user_id, tweet_id=id)
        session.add(new_like)
        session.commit()
    response = {"result": True}
    logger.debug(f"User (ID: {user_id}) liked Tweet (ID: {id})")
    return jsonify(response)


@swag_from("docs/delete_like.yml")
@app.route("/api/tweets/<id>/likes", methods=["DELETE"])
def delete_like(user_id: UserIdDepend, id: int) -> flask.wrappers.Response:
    """
    Endpoint для удаления лайков
    :param id: int
    :return: Response
    """
    if liked(user_id, id):
        like = session.query(Like).filter(
            and_(Like.user_id == user_id, Like.tweet_id == id)
        )
        session.delete(like.one())
        session.commit()
    response = {"result": True}
    logger.debug(f"User (ID: {user_id}) deleted liked from Tweet (ID: {id})")
    return jsonify(response)


@swag_from("docs/follow_user.yml")
@app.route("/api/users/<id>/follow", methods=["POST"])
def follow_user(user_id: UserIdDepend, id: int) -> flask.wrappers.Response:
    """
    Endpoint для добавления подписок
    :param id: int
    :return: Response
    """
    if not followed(user_id, id):
        new_follow = Follow(following_user_id=user_id, followed_user_id=id)
        session.add(new_follow)
        session.commit()
    response = {"result": True}
    logger.debug(f"User (ID: {user_id}) followed User (ID: {id})")
    return jsonify(response)


@swag_from("docs/delete_follow.yml")
@app.route("/api/users/<id>/follow", methods=["DELETE"])
def delete_follow(user_id: UserIdDepend, id: int) -> flask.wrappers.Response:
    """
    Endpoint для удаления подписок
    :param id: int
    :return: Response
    """
    if followed(user_id, id):
        follow = session.query(Follow).filter(
            and_(Follow.following_user_id == user_id, Follow.followed_user_id == id)
        )
        session.delete(follow.one())
        session.commit()
    response = {"result": True}
    logger.debug(f"User (ID: {user_id}) deleted follow from User (ID: {id})")
    return jsonify(response)


@swag_from("docs/get_tweets.yml")
@app.route("/api/tweets/", methods=["GET"])
def get_tweets(user_id: UserIdDepend) -> flask.wrappers.Response:
    """
    Endpoint для отображения твитов в ленте
    :return: Response
    """
    try:
        response = show_tweets(user_id)
        logger.debug(f"User (ID: {user_id}) requested Tweets")
        return jsonify(response)
    except Exception as exc:
        response = {
            "result": False,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        logger.error(f"User (ID: {user_id}) got Error while getting Tweets")
        return jsonify(response)


@swag_from("docs/my_profile.yml")
@app.route("/api/users/me", methods=["GET"])
def my_profile(user_id: UserIdDepend) -> flask.wrappers.Response:
    """
    Endpoint для отображения собственного профиля
    :return: Response
    """
    response = show_profile(user_id)
    logger.debug(f"User (ID: {user_id}) visited his profile")
    return jsonify(response)


@swag_from("docs/get_profile.yml")
@app.route("/api/users/<id>", methods=["GET"])
def get_profile(user_id: UserIdDepend, id: int) -> flask.wrappers.Response:
    """
    Endpoint для отображения выбранного профиля
    :param id: int
    :return: Response
    """
    response = show_profile(id)
    logger.debug(f"User (ID: {user_id}) visited profile of User (ID: {id})")
    return jsonify(response)


FlaskInjector(app=app, modules=[configure])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
