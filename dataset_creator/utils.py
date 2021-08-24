import datetime as dt
from hashlib import sha256
from typing import List, Tuple


def get_id_and_name(sensor: str) -> Tuple[str, int]:
    splitted_sensor: List[str] = sensor.split("_")
    return splitted_sensor[0], int(splitted_sensor[1])


def convert_timestamp_format(timestamp: str) -> str:
    date = dt.datetime.strptime(timestamp, "%H:%M:%S %d.%m.%Y")
    return dt.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")


def get_dataset_hash(
    sensors: List[str], start_timestamp: str, end_timestamp: str
) -> str:
    sensors_copy: List[str] = sorted(sensors.copy())
    sensors_copy.append(start_timestamp)
    sensors_copy.append(end_timestamp)
    string_to_hash: str = "".join(sensors_copy)
    return sha256(string_to_hash.encode("utf-8")).hexdigest()
