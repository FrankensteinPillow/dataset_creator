from pydantic import BaseSettings
from functools import lru_cache
from os import environ


class Config(BaseSettings):
    db_url: str = environ.get("db_url", "")
    raw_data_path: str = environ.get("raw_data_path", "")
    result_data_path: str = environ.get("result_data_path", "")


@lru_cache
def get_config() -> Config:
    return Config()
