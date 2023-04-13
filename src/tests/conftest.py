import pytest
from flask.testing import FlaskClient

from src.app import app
from src.models import Tweet, User, session


@pytest.fixture
def test_app():
    yield app


@pytest.fixture
def _session():
    yield session


@pytest.fixture
def mock_user():
    mock_user = User(name="mockname", api_key="testtest")
    session.add(mock_user)
    session.commit()
    yield mock_user
    session.delete(mock_user)
    session.commit()


@pytest.fixture
def mock_headers(mock_user):
    return {"api-key": mock_user.api_key}


@pytest.fixture
def mock_user_2():
    mock_user_2 = User(name="mockname2", api_key="testtest2")
    session.add(mock_user_2)
    session.commit()
    yield mock_user_2
    session.delete(mock_user_2)
    session.commit()


@pytest.fixture
def mock_tweet(mock_user):
    mock_tweet = Tweet(text="Hello World", user_id=mock_user.id)
    session.add(mock_tweet)
    session.commit()
    yield mock_tweet
    session.delete(mock_tweet)
    session.commit()


@pytest.fixture
def client(test_app):
    client: FlaskClient = app.test_client()
    client.post()
    yield client
