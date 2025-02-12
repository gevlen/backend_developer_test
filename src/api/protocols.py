from typing import List
from datetime import date

from src.user.models import UserResponseV1, UserAddRequestV1, UserStatsResponseV1


class UserServiceProtocol:
    def get_all_users(self) -> List[UserResponseV1]:
        raise NotImplementedError

    def get_user_by_id(self, id: int) -> UserResponseV1:
        raise NotImplementedError

    def get_user_stats_by_date(self,
                               id: int, date_from: date, date_to: date
                               ) -> UserStatsResponseV1:
        raise NotImplementedError

    def add_user(self, user: UserAddRequestV1) -> None:
        raise NotImplementedError

    def delete_user_by_id(self, id: int) -> None:
        raise NotImplementedError

