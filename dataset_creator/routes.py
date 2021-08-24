from fastapi import responses
from main import app
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from models import CreateDatasetResponse, CreateDatasetBody
from datasets import create_dataset


@app.post("/datasets/create", response_model=CreateDatasetResponse)
async def create_ds(body: CreateDatasetBody):
    # response = CreateDatasetResponse(message="ok", file_path="/home/user")
    response = await create_dataset(body)
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )
