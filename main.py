from fastapi import FastAPI
from pydantic import BaseModel
from config.dummy_log_config import log_messages, get_random_log_type
from config.logging_config import get_logger 
from typing import List
import asyncio
import random
import time
import uvicorn

app = FastAPI()
logger = get_logger()

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str

dummy_logs: List[dict] = []

def generate_dummy_log() -> dict:
    log_type = get_random_log_type()
    message = random.choice(log_messages[log_type])
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return {"timestamp": timestamp, "level": log_type, "message": message}

async def periodic_log_generator(interval: int = 5):
    while True:
        new_log = generate_dummy_log()
        dummy_logs.append(new_log)
        log_message = f"{new_log['timestamp']} [{new_log['level']}] {new_log['message']}"

        if new_log["level"] == "ERROR":
            logger.error(log_message)
        elif new_log["level"] == "WARNING":
            logger.warning(log_message)
        elif new_log["level"] == "DEBUG":
            logger.debug(log_message)
        else:
            logger.info(log_message)

        await asyncio.sleep(interval)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_log_generator(5))

@app.get("/logs", response_model=List[LogEntry])
def get_logs():
    return dummy_logs

@app.post("/log")
def add_log(log: LogEntry):
    dummy_logs.append(log.dict())
    log_message = f"{log.timestamp} [{log.level}] {log.message}"
    logger.info(log_message)
    return {"message": "Log added", "log": log}

class LogBatch(BaseModel):
    logs: List[LogEntry]

@app.post("/logs/batch")
def add_logs_batch(batch: LogBatch):
    for log in batch.logs:
        dummy_logs.append(log.dict())
        log_message = f"{log.timestamp} [{log.level}] {log.message}"
        logger.info(log_message)
    return {"message": f"{len(batch.logs)} logs added successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)