import uvicorn
from config import get_config

CONFIG = get_config()

uvicorn.run(
    app="main:app", port=CONFIG.service_port, log_level=CONFIG.log_level
)
