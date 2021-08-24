import uvicorn

uvicorn.run(app="main:app", port=3520, log_level="debug")
