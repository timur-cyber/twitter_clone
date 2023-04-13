from flask import request
from injector import Injector, inject

from src.models import SessionLocal, User


class UserIdDepend(Injector):
    @inject
    def get_user_id_by_api_key(self) -> int:
        session = SessionLocal()
        api_key = request.headers.get("api-key")
        user = session.query(User).filter(User.api_key == api_key).one()
        session.close()
        return user.id


def configure(binder):
    binder.bind(UserIdDepend, to=UserIdDepend().get_user_id_by_api_key, scope=request)
