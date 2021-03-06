from typing import Dict

import pandas as pd
import pyarrow
import pyarrow.parquet as pq

import config
import sql
import utils
from exceptions import DataNotFound
from models import CreateDatasetBody

CONFIG = config.get_config()


async def create_dataset(request_body: CreateDatasetBody) -> Dict[str, str]:
    sensors_data = []
    start_timestamp: str = request_body.start_timestamp
    end_timestamp: str = request_body.end_timestamp
    dataset_hash = utils.get_dataset_hash(
        request_body.sensors, start_timestamp, end_timestamp
    )
    res = await sql.get_dataset_id_by_hash(dataset_hash)
    if res:
        dataset_id = res[0]
        result_file_name = f"dataset_{dataset_id}.parquet"
        return {"message": "ok", "filename": result_file_name}
    for sensor in request_body.sensors:
        sensor_name, sensor_id = utils.get_id_and_name(sensor)
        data = await sql.get_sensors_data(
            sensor_name, sensor_id, start_timestamp, end_timestamp
        )
        if not data:
            msg: str = (
                f"Not found data for sensor '{sensor_name}_{sensor_id}' and "
                f"timestamps {start_timestamp} {end_timestamp}"
            )
            raise DataNotFound(msg)
        sensors_data.append((data, sensor_name, sensor_id))
    result = concatenate_data(sensors_data)
    table = pyarrow.Table.from_pandas(result)
    dataset_id = await sql.add_dataset(
        start_timestamp, end_timestamp, dataset_hash
    )
    await write_datasets_link(sensors_data, dataset_id)
    result_file_name = f"dataset_{dataset_id}.parquet"
    pq.write_table(table, f"{CONFIG.result_data_path}/{result_file_name}")
    return {"message": "ok", "filename": result_file_name}


async def write_datasets_link(sensors_data, dataset_id):
    dataset_links = []
    for sensor_data, sensor_name, sensor_id in sensors_data:
        for _, timestamp, __ in sensor_data:
            dataset_links.append(
                {
                    "dataset_id": dataset_id,
                    "sensor_name": sensor_name,
                    "sensor_id": sensor_id,
                    "timestamp": timestamp,
                }
            )
    await sql.add_dataset_link(dataset_links)


def concatenate_data(sensors_data):
    sensor_frames = []
    for sensors_group, sensor_name, sensor_id in sensors_data:
        frames = []
        for sensor in sensors_group:
            df = pq.read_table(
                source=f"{CONFIG.raw_data_path}/{sensor['filename']}"
            ).to_pandas()
            frames.append(df)
        result = pd.concat(frames), sensor_name, sensor_id
        sensor_frames.append(result)
    result = pd.DataFrame({})
    for i, (frame, sensor_name, sensor_id) in enumerate(sensor_frames):
        result.insert(i, f"{sensor_name}_{sensor_id}", frame["values"])
    return result
