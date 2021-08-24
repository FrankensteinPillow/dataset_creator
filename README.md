# Dataset preprocessor
Web service for data preprocessing

## Installation and Launch
You can use Dockerfile to build docker-container for deploy and run this service.

to build container:
```bash
docker build -t dataset_creator .
```
to run container:
```bash
docker run --rm --env-file envfile -p 3520:3520 --name dataset_creator -d -v /home/user/path/to/db:/home/user/db --net=host dataset_creator
```
The service uses a sqlite database file so it must be mounted in the container so we use the "-v" flag when running.

We also use a file with environment variables to configure the service. This file contains options that are strictly necessary for the service, including the path to the directory with the database. You can define any desired values for these variables, but it is important that the value of the db_url variable is consistent with the directory being mounted.

It is better to place the raw data in a directory next to the database file, this will allow it to be limited to one mount flag. However, if different directories need to be configured, this can be solved using environment variables.

During development, I simply mounted the directory from the zip archive passed as a test task.

The result of the work of requests to the service will be parquet files, in order for them to be accessed from outside the container, you need to mount the directory and specify the appropriate settings in the file with environment variables.
```bash
-v /home/user/some_directory:/home/user/some_directory
```
In envfile:
```
raw_data_path=/home/user/db/raw_data
result_data_path=/home/user/some_directory
```

The service runs on port 3520 by default, but this behavior can be changed using environment variables.

## Documentation
When the service starts, the documentation will be available in swagger_ui or redoc. Check address `127.0.0.1:3520/docs` or `127.0.0.1:3520/redoc`

We have one POST endpoint to create a dataset `127.0.0.1:3520/datasets/create`. For a general description of this endpoint and a description of the request body, see the documentation.