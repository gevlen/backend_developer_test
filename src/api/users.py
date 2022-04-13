from typing import List
from datetime import date

from fastapi import APIRouter, status, Depends, Path

from src.api.protocols import UserServiceProtocol
from src.user.models import UserResponseV1, UserAddRequestV1

router = APIRouter(
    tags=['Users']
)


@router.get(
    path='/v1/users',
    response_model=List[UserResponseV1],
    summary='Список пользователей',
    description='Возвращает список всех пользователей.'
)
def get_all_users(
        user_service: UserServiceProtocol = Depends()
):
    return user_service.get_all_users()


@router.get(
    path='/v1/users/{id}',
    response_model=UserResponseV1,
    summary='Информация о пользователе',
    description='Возвращает информацию о пользователе.'
)
def get_user(
        id: int = Path(..., ge=1),
        user_service: UserServiceProtocol = Depends()
):
    return user_service.get_user_by_id(id)


@router.put(
    path='/v1/users',
    status_code=status.HTTP_201_CREATED,
    summary='Добавить пользователя',
    description='Добавляет пользователя для отслеживания популярности репозиториев.',
)
def add_user(
        user_data: UserAddRequestV1,
        user_service: UserServiceProtocol = Depends()
):
    user_service.add_user(user_data)


@router.delete(
    path='/v1/users/{id}',
    summary='Удалить пользователя',
    description='Удаляет пользователя.'
)
def delete_user(
        id: int = Path(..., ge=1),
        user_service: UserServiceProtocol = Depends()
):
    user_service.delete_user_by_id(id)

@router.get(
    path='/v1/users/{id}/stats',
    summary='Информация о пользователе за указанный период',
    description='Выводит информацию о пользователе за указанный период',
)
def get_user_stats_by_id_and_date(
        id: int = Path(..., ge=1),
        date_from: date = Path(...),
        date_to: date = Path(...),
        user_service: UserServiceProtocol = Depends()
):
    return user_service.get_user_stats_by_date(id, date_from, date_to)
