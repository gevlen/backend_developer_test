import sqlalchemy as sa
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from src.api import users, protocols
from src.database import DatabaseSettings, create_database_url
from src.user.service import UserService
from src.parser import stats


def get_application() -> FastAPI:
    application = FastAPI(
        title='GitHub Repo Stats',
        description='Сервис сбора статистических данных о популярности репозиториев на GitHub.',
        version='1.0.0'
    )

    application.include_router(users.router)

    db_settings = DatabaseSettings()
    engine = sa.create_engine(
        create_database_url(db_settings),
        future=True
    )
    user_service = UserService(engine)
    application.dependency_overrides[protocols.UserServiceProtocol] = lambda: user_service
    return application


app = get_application()

@app.on_event('startup')
@repeat_every(seconds=60 * 60 * 24)
def parse_on_start() -> None:
    service = stats.ParserGitHub(engine=None)
    service.parse()