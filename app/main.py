from app.utils.logger import setup_logger
from fastapi import FastAPI


logger = setup_logger(__name__)

app = FastAPI()


@app.get("/")
def read_root():
    logger.info("Root endpoint called.")
    return {"message": "Hello, world!"}
