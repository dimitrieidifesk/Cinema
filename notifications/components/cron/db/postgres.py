import datetime
import uuid

import asyncpg
import backoff
from asyncpg.exceptions import CannotConnectNowError, TooManyConnectionsError
from core.config import postgres_settings


class PostgreSQLConsumer:
    def __init__(self, connection) -> None:
        self.connection: asyncpg.connection = connection

    @backoff.on_exception(
        backoff.expo, (TooManyConnectionsError, CannotConnectNowError), max_tries=5, max_time=10
    )
    async def insert_task(
        self,
        data: dict,
        users_category=postgres_settings.USERS_CATEGORY_FOR_LIKE_NOTIFICATIONS,
        template_id=postgres_settings.LIKES_TEMPLATE_ID,
        pending_time=datetime.datetime.now(),
    ):
        return await self.connection.fetch(
            "INSERT INTO {} (template_id_id, task_name, users_category_id, data, pending_time, created, updated_at, id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)".format(
                postgres_settings.TASKS_TABLE
            ),
            template_id,
            "Like on user's review",
            users_category,
            str(data),
            pending_time,
            datetime.datetime.now(),
            datetime.datetime.now(),
            uuid.uuid4(),
        )
