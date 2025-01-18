import datetime
import pytest

from timezones.favourite_timezones import FavouriteTimezone
from tests.constants import TIMEZONE_NAMES

@pytest.mark.parametrize("timezone_name", TIMEZONE_NAMES)
def test_favourite_timezone(timezone_name: str):
    tz = FavouriteTimezone(timezone_name)
    tz_utc = tz.get_time().astimezone(datetime.timezone.utc)
    now = datetime.datetime.now().astimezone(datetime.timezone.utc)

    # microsecond field will differ
    format = "%Y %B %d %H:%M:%S %Z %z %c %x %X"
    assert tz_utc.strftime(format) == now.strftime(format)
    assert tz_utc.tzinfo == now.tzinfo


def test_get_time():
    format = "%Y-%m-%d %H:%M %Z %z"
    tz = FavouriteTimezone("Europe/London")
    time = datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
    assert tz.get_time(time).strftime(format) == "2021-01-01 00:00 GMT +0000"
    assert tz.get_time().strftime(format) == datetime.datetime.now(
        tz.timezone
    ).strftime(format)
