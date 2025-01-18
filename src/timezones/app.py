import pytz
import datetime

import timezones.parser as parser
from timezones.logger import app_logger
from timezones.favourite_timezones import FavouriteTimezonesManager


def main():
    app_logger.debug("Starting main function")

    # Create a manager for favourite timezones
    manager = FavouriteTimezonesManager()

    # Add some favourite timezones

    TIMEZONE_NAMES = [
        "Europe/London",
        "Europe/Paris",
        "America/New_York",
        "America/Los_Angeles",
        "Asia/Tokyo",
        "Australia/Sydney",
    ]
    for timezone_name in TIMEZONE_NAMES:
        manager.add_timezone(timezone_name)

    # Display all favourite timezones
    manager.display_timezones(
        utc=True, city=True, region=True, time=datetime.datetime(2021, 1, 1, 0, 0)
    )


if __name__ == "__main__":
    app_logger.debug("Running main")
    main()
    app_logger.debug("Finished running main")
