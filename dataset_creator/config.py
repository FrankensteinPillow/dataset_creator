from functools import lru_cache
from os import environ

from pydantic import BaseSettings


class Config(BaseSettings):
    db_url: str = environ.get("db_url", "")
    raw_data_path: str = environ.get("raw_data_path", "")
    result_data_path: str = environ.get("result_data_path", "")
    service_port: str = environ.get("service_port", "")
    log_level: str = environ.get("log_level", "")


@lru_cache
def get_config() -> Config:
    return Config()
