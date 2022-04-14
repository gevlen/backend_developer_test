import httpx
from sqlalchemy import insert, select
from sqlalchemy.engine import Engine

from src.user.service import UserService


class ParserGitHub:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._user_service = UserService(engine)

    def parse(self):
        users = self._user_service.get_all_users()
        user_stats = self.get_stats([user.login for user in users])
        self.upload_to_database(user_stats)

    def upload_to_database(self, user_stats):
        pass

    def get_stats(self, lst):
        pass

