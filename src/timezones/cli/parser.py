import typer
import os
from contextlib import contextmanager
from pathlib import Path

import timezones

app = typer.Typer()


@app.command()
def version():
    "Returns the version of the timezones application"
    print(timezones.__version__)


def get_db_path():
    db_path_env = os.getenv("TIMEZONES_DB_PATH", "")
    if db_path_env:
        return Path(db_path_env)
    else:
        return Path.home() / ".timezones.db"


@contextmanager
def get_db():
    path = get_db_path()
