import typer

from timezones.app import app
from timezones.database.favourite_timezones import FavouriteTimezonesManager
from timezones.utils.constants import DB_PATH

@app.command()
def add(city: str):
    ft_manager = FavouriteTimezonesManager(DB_PATH)
    ft_manager.add_timezone(city)