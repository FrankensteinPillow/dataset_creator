from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from datasets import create_dataset
from exceptions import DataNotFound
from main import app
from models import CreateDatasetBody, CreateDatasetError, CreateDatasetResponse


@app.post(
    "/datasets/create",
    responses={
        200: {"model": CreateDatasetResponse},
        404: {"model": CreateDatasetError},
    },
)
async def create_ds(body: CreateDatasetBody):
    """Preprocess dataset. Concatenate data from multiple sensors by id and
    timestamp. Return filename of parquet file with preprocessed table.
    """
    try:
        result = await create_dataset(body)
        response: CreateDatasetResponse = CreateDatasetResponse(
            message=result["message"], file_path=result["filename"]
        )
        return JSONResponse(
            content=jsonable_encoder(response),
            status_code=status.HTTP_200_OK,
            media_type="application/json",
        )
    except DataNotFound as error:
        error_response: CreateDatasetError = CreateDatasetError(
            message=error.msg,
            status_code=status.HTTP_404_NOT_FOUND,
            details={},
        )
        return JSONResponse(
            content=jsonable_encoder(error_response),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )
