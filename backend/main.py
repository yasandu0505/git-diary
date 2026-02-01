from fastapi import FastAPI
from routes import all_routers
from settings import setup_logging
import logging

setup_logging()


logger = logging.getLogger(__name__)

app = FastAPI(title="Git Diary")

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")

for router, prefix, tags in all_routers:
    app.include_router(router, prefix=prefix, tags=tags)
