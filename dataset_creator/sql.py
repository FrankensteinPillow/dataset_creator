from typing import Any, Dict, Mapping, Optional

import databases as db
import sqlalchemy

from config import get_config
from main import app

CONFIG = get_config()

database = db.Database(CONFIG.db_url)
metadata = sqlalchemy.MetaData()

datasets = sqlalchemy.Table(
    "datasets",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.Integer, primary_key=True, autoincrement=True
    ),
    sqlalchemy.Column("start_timestamp", sqlalchemy.Text),
    sqlalchemy.Column("end_timestamp", sqlalchemy.Text),
    sqlalchemy.Column("dataset_hash", sqlalchemy.Text),
)
dataset_to_sensors = sqlalchemy.Table(
    "datasets_to_sensors",
    metadata,
    sqlalchemy.Column("dataset_id", sqlalchemy.Integer),
    sqlalchemy.Column("sensor_name", sqlalchemy.Text),
    sqlalchemy.Column("sensor_id", sqlalchemy.Integer),
    sqlalchemy.Column("timestamp", sqlalchemy.Text),
)
alpha_sensors = sqlalchemy.Table(
    "alpha_sensors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer),
    sqlalchemy.Column("timestamp", sqlalchemy.Text),
    sqlalchemy.Column("filename", sqlalchemy.Text),
)
beta_sensors = sqlalchemy.Table(
    "beta_sensors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer),
    sqlalchemy.Column("timestamp", sqlalchemy.Text),
    sqlalchemy.Column("filename", sqlalchemy.Text),
)
gamma_sensors = sqlalchemy.Table(
    "gamma_sensors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer),
    sqlalchemy.Column("timestamp", sqlalchemy.Text),
    sqlalchemy.Column("filename", sqlalchemy.Text),
)
delta_sensors = sqlalchemy.Table(
    "delta_sensors",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer),
    sqlalchemy.Column("timestamp", sqlalchemy.Text),
    sqlalchemy.Column("filename", sqlalchemy.Text),
)
sensors: Dict[str, sqlalchemy.Table] = {
    "alpha": alpha_sensors,
    "beta": beta_sensors,
    "gamma": gamma_sensors,
    "delta": delta_sensors,
}
engine = sqlalchemy.create_engine(
    CONFIG.db_url, connect_args={"check_same_thread": False}
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def get_sensors_data(
    sensor_name: str, sensor_id: int, start_timestamp: str, end_timestamp: str
):
    sensor = sensors[sensor_name]
    query = (
        sensor.select()
        .where(sensor.c.id == sensor_id)
        .where(sensor.c.timestamp >= start_timestamp)
        .where(sensor.c.timestamp <= end_timestamp)
    )
    return await database.fetch_all(query)


async def add_dataset(
    start_timestamp: str, end_timestamp: str, dataset_hash: str
):
    query = datasets.insert().values(
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        dataset_hash=dataset_hash,
    )
    return await database.execute(query)


async def add_dataset_link(dataset_links):
    query = dataset_to_sensors.insert().values(dataset_links)
    await database.execute(query)


async def get_dataset_id_by_hash(
    dataset_hash: str,
) -> Optional[Mapping[Any, Any]]:
    query = datasets.select().where(datasets.c.dataset_hash == dataset_hash)
    return await database.fetch_one(query)
