from typing import List
from datetime import date

from sqlalchemy import select, insert, delete, and_
from sqlalchemy.future import Engine

from src.database import tables
from src.user.models import UserResponseV1, UserAddRequestV1, UserStatsResponseV1, StatsResponseV1


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def get_all_users(self) -> List[UserResponseV1]:
        query = select(tables.users)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        users = []
        for user_data in users_data:
            user = UserResponseV1(
                id=user_data['id'],
                login=user_data['login'],
                name=user_data['name']
            )
            users.append(user)
        return users

    def get_user_by_id(self, id: int) -> UserResponseV1:
        query = select(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            user_data = connection.execute(query)
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        return user

    def add_user(self, user: UserAddRequestV1) -> None:
        query = insert(tables.users).values(
            id=user.id,
            login=user.login,
            name=user.name
        )
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def delete_user_by_id(self, id: int) -> None:
        query = delete(tables.users).where(tables.users.c.id == id)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def get_stats_user_by_date(self, id: int, date_from: date, date_to: date) -> UserStatsResponseV1:
        user_query = select(tables.users).where(tables.users.c.id == id)
        stats_query = select(tables.stats).where(
            and_(
                tables.stats.c.user_id == id,
                date_from <= tables.stats.c.date <= date_to)
            ).order_by(tables.stats.c.repo_id, tables.stats.c.date)
        with self._engine.connect() as connection:
            user_data = connection.execute(user_query)
            stats_data = connection.execute(stats_query)
        user = UserResponseV1(
            id=user_data['id'],
            login=user_data['login'],
            name=user_data['name']
        )
        stats = []
        for data in stats_data:
            stat = StatsResponseV1(
                repo_id=data['repo_id'],
                date=data['date'],
                stargazers=data['stargazers'],
                forks=data['forks'],
                watchers=data['watchers'],
            )
            stats.append(stat)
        return UserStatsResponseV1(user=user, stats=stats)

