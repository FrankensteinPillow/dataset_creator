from typing import Tuple, List
import datetime as dt
from hashlib import sha256


def get_id_and_name(sensor: str) -> Tuple[str, int]:
    sensor = sensor.split("_")
    return sensor[0], int(sensor[1])


def convert_timestamp_format(timestamp: str) -> str:
    date = dt.datetime.strptime(timestamp, "%H:%M:%S %d.%m.%Y")
    return dt.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")


def get_dataset_hash(
    sensors: List[str], start_timestamp: str, end_timestamp: str
) -> str:
    sensors_copy = sorted(sensors.copy())
    sensors_copy.append(start_timestamp)
    sensors_copy.append(end_timestamp)
    sensors_copy = "".join(sensors_copy)
    return sha256(sensors_copy.encode("utf-8")).hexdigest()
