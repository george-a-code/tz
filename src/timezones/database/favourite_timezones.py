import datetime
import pytz
from dataclasses import asdict, dataclass, field
from typing import List, Optional

from timezones.database.database import TimezoneDatabase


@dataclass
class FavouriteTimezone:
    timezone_name: str
    region: Optional[str] = field(default=None)
    city: Optional[str] = field(default=None)
    timezone: Optional[datetime.tzinfo] = field(default=None)
    id: Optional[int] = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, data: dict) -> "FavouriteTimezone":
        # Convert timezone to pytz object for easier serialization
        data["timezone"] = pytz.timezone(data["timezone"])
        instance = FavouriteTimezone(**data)
        instance.__post_init__()
        return instance

    def to_dict(self) -> dict:
        data = asdict(self)
        data["timezone"] = self.timezone.zone  # convert to str for json serialization
        return data

    def get_time(self, time: datetime.datetime = None) -> datetime.datetime:
        if time is None:
            time = datetime.datetime.now()
        elif time.tzinfo is None:
            # Assume naive datetime is in UTC
            time = pytz.utc.localize(time)
        # Convert time to self.timezone
        new_time = time.astimezone(self.timezone)
        return new_time

    def __post_init__(self) -> None:
        if self.timezone is None:
            self.timezone = pytz.timezone(self.timezone_name)
        if self.region is None:
            self.region = self.timezone_name.split("/")[0]
        if self.city is None:
            self.city = self.timezone_name.split("/")[1]

    def __str__(self):
        return f"{self.city}, {self.region} - {self.timezone}"


class FavouriteTimezonesManager:
    def __init__(self, db_path):
        self._dp_path = db_path
        self._db = TimezoneDatabase(db_path)

    def add_timezone(self, timezone_name) -> None:
        timezone = FavouriteTimezone(timezone_name)
        id = self._db.create(timezone.to_dict())
        self._db.update(id, {"id": id})

    def remove_timezone(
        self, *, city: str = None, tz_name: str = None, tz_id: int = None
    ) -> None:
        if tz_id:
            self._db.remove(tz_id)
        elif city:
            tz_id = self._db.get_timezone(city)["id"]
            self._db.remove(tz_id)
        elif tz_name:
            city = tz_name.split("/")[1]
            tz_id = self._db.get_timezone(city)["id"]
            self._db.remove(tz_id)
        else:
            raise ValueError("You must provide either city, tz_name or tz_id")

    def list_timezones(
        self,
        timezones_names: List[str] = None,
    ) -> List:
        all_timezones = self._db.get_all()
        if timezones_names is None:
            timezones = [FavouriteTimezone.from_dict(tz) for tz in all_timezones]
        else:
            timezones = [
                FavouriteTimezone.from_dict(tz)
                for tz in all_timezones
                if tz["timezone_name"] in timezones_names
            ]
        return timezones

    def close(self) -> None:
        self._db.close()
