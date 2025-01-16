import datetime
import pytz
from tabulate import tabulate

from timezones.logger import app_logger


class FavouriteTimezone:
    def __init__(self, timezone_name):
        self.timezone_name = timezone_name
        self.timezone = pytz.timezone(timezone_name)
        self.region = self.timezone_name.split("/")[0]
        self.city = self.timezone_name.split("/")[1]

        app_logger.debug(f"Favourite timezone set to {timezone_name}")

    def get_time(self, time: datetime.datetime = None) -> datetime.datetime:
        if time is None:
            time = datetime.datetime.now(pytz.utc)
        elif time.tzinfo is None:
            # Assume naive datetime is in UTC
            time = pytz.utc.localize(time)
        # Convert time to self.timezone
        new_time = time.astimezone(self.timezone)
        return new_time

    def __str__(self):
        return f"{self.get_time()}"


class FavouriteTimezonesManager:

    default_datetime_format = "%m-%d %H:%M"

    def __init__(self, datetime_format: str = None):
        self.datetime_format = datetime_format or self.default_datetime_format
        self.favourite_timezones = []

    def add_timezone(self, timezone_name: str):
        self.favourite_timezones.append(FavouriteTimezone(timezone_name))
        app_logger.info(f"Added favourite timezone: {timezone_name}")

    def remove_timezone(self, timezone_name: str):
        self.favourite_timezones = [
            tz for tz in self.favourite_timezones if tz.timezone_name != timezone_name
        ]
        app_logger.info(f"Removed favourite timezone: {timezone_name}")

    def display_timezones(
        self,
        time: datetime = None,
        utc: bool = False,
        city: bool = False,
        region: bool = False,
    ):
        if time is None:
            time = datetime.datetime.now()
        columns = [
            ("City", lambda tz: tz.city) if city else None,
            ("Region", lambda tz: tz.region) if region else None,
            (  # this column not optional
                f"Time at {time.strftime(self.datetime_format)}",
                lambda tz: tz.get_time().strftime(f"{self.datetime_format} %Z"),
            ),
            (("UTC Offset", lambda tz: tz.get_time().strftime("%z")) if utc else None),
        ]
        columns = [column for column in columns if column is not None]
        headers = [column[0] for column in columns]
        table = [
            [column[1](tz) for column in columns] for tz in self.favourite_timezones
        ]
        print(tabulate(table, headers))
