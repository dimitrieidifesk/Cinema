import logging

import uvicorn
from core.config import config
from core.logger import LOGGING
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


db = SQLAlchemy()


def init_db(app: Flask):
    db_name = config.AUTH_POSTGRES_DB
    db_user = config.AUTH_POSTGRES_USER
    db_pass = config.AUTH_POSTGRES_PASSWORD
    db_host = config.AUTH_POSTGRES_HOST
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
    db.init_app(app)


if __name__ == "__main__":
    init_db(app)
    app.run()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )