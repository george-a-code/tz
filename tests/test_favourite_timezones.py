import datetime
import os
import pytest
from typing import List, Dict

from timezones.favourite_timezones_db import (
    FavouriteTimezone,
    FavouriteTimezonesManager,
)

TIMEZONE_NAMES = [
    "Europe/London",
    "Europe/Paris",
    "America/New_York",
    "America/Los_Angeles",
    "Asia/Tokyo",
    "Australia/Sydney",
]


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


def test_adding_timezone(test_db_path, timezone_names: List[str] = TIMEZONE_NAMES):
    manager = FavouriteTimezonesManager(db_path=test_db_path)

    for timezone_name in timezone_names:
        manager.add_timezone(timezone_name)

    assert [
        any(tz.timezone_name == name for tz in manager.list_timezones())
        for name in timezone_names
    ]


def test_removing_timezone(test_db_path, timezone_names: List[str] = TIMEZONE_NAMES):
    manager = FavouriteTimezonesManager(test_db_path)

    for timezone_name in timezone_names:
        manager.add_timezone(timezone_name)

    for timezone_name in timezone_names:
        manager.remove_timezone(tz_name=timezone_name)

    assert [
        all(tz.timezone_name != name for tz in manager.favourite_timezones)
        for name in timezone_names
    ]


@pytest.mark.parametrize(
    "display_kwargs",
    [
        {"city": True},
        {"region": True},
        {"utc": True},
        {"city": True, "region": True},
        {"city": True, "utc": True},
        {"region": True, "utc": True},
        {"city": True, "region": True, "utc": True},
    ],
    ids=[
        "city_only",
        "region_only",
        "utc_only",
        "city_region",
        "city_utc",
        "region_utc",
        "all",
    ],
)
def test_display_timezones(
    test_db_path,
    capsys,
    display_kwargs: Dict[str, str],
    timezone_names: List[str] = TIMEZONE_NAMES,
):
    os.environ["LOG_LEVEL"] = "CRITICAL"  # Disable logging to keep output clean
    manager = FavouriteTimezonesManager(test_db_path)
    for timezone_name in timezone_names:
        manager.add_timezone(timezone_name)

    manager.display_timezones(**display_kwargs)
    captured = capsys.readouterr()
    print(captured.out)
    # Verify the correct rows/columns are displayed
    assert "Time at" in captured.out
    if display_kwargs.get("city"):
        assert "City" in captured.out
    if display_kwargs.get("region"):
        assert "Region" in captured.out
    if display_kwargs.get("utc"):
        assert "UTC Offset" in captured.out

    for timezone_name in timezone_names:
        if display_kwargs.get("city"):
            city = timezone_name.split("/")[1]
            assert city in captured.out
        if display_kwargs.get("region"):
            region = timezone_name.split("/")[0]
            assert region in captured.out

    # Cleanup
    del os.environ["LOG_LEVEL"]


def test_display_future_time(test_db_path, capsys, timezone_names=TIMEZONE_NAMES):
    manager = FavouriteTimezonesManager(test_db_path)
    for timezone_name in timezone_names:
        manager.add_timezone(timezone_name)

    manager.display_timezones(time=datetime.datetime(2022, 1, 1, 0, 0))
    captured = capsys.readouterr()
    assert "Time at 01-01 00:00" in captured.out

    manager.display_timezones(time=datetime.datetime(2026, 6, 5, 2, 7))
    captured = capsys.readouterr()
    assert "Time at 06-05 02:07" in captured.out
