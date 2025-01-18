import datetime
import os
import pytest
from typing import List, Dict

from timezones.favourite_timezones import FavouriteTimezonesManager


def test_adding_timezone(test_db_path, timezone_example_list):
    manager = FavouriteTimezonesManager(db_path=test_db_path)

    for timezone_name in timezone_example_list:
        manager.add_timezone(timezone_name)

    assert [
        any(tz.timezone_name == name for tz in manager.list_timezones())
        for name in timezone_example_list
    ]


def test_removing_timezone(test_db_path, timezone_example_list):
    manager = FavouriteTimezonesManager(test_db_path)

    for timezone_name in timezone_example_list:
        manager.add_timezone(timezone_name)

    for timezone_name in timezone_example_list:
        manager.remove_timezone(tz_name=timezone_name)

    assert [
        all(tz.timezone_name != name for tz in manager.list_timezones())
        for name in timezone_example_list
    ]