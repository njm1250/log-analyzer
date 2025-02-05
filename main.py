from fastapi import FastAPI
from pydantic import BaseModel
from config.dummy_log_config import log_messages, get_random_log_type
from config.logging_config import get_logger
from utils.log_preprocessor import preprocess_logs
from typing import List, Optional
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
    stacktrace: Optional[str] = None

dummy_logs: List[dict] = []

# 비동기 큐 나중에 kafka나 RabbitMQ로 대체가능
log_queue = asyncio.Queue()

def generate_dummy_log() -> dict:
    log_type = get_random_log_type()
    message = random.choice(log_messages[log_type])
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = {"timestamp": timestamp, "level": log_type, "message": message}
    if log_type == "ERROR":
        log["stacktrace"] = "Dummy stacktrace for error"  
    return log

async def periodic_log_generator(interval: int = 5):
    while True:
        new_log = generate_dummy_log()
        dummy_logs.append(new_log)

        await log_queue.put(new_log)

        log_message = f"{new_log['timestamp']} [{new_log['level']}] {new_log['message']}"
        if "stacktrace" in new_log:
            log_message += f"\nStackTrace:\n{new_log['stacktrace']}"

        if new_log["level"] == "ERROR":
            logger.error(log_message)
        elif new_log["level"] == "WARNING":
            logger.warning(log_message)
        elif new_log["level"] == "DEBUG":
            logger.debug(log_message)
        else:
            logger.info(log_message)

        await asyncio.sleep(interval)

# LLM API 예시
async def call_llm_api(error_log: dict) -> str:
    await asyncio.sleep(1)  
    return f"Suggested solution for: {error_log['message']}"

# 알림전송 예시
def send_alert(error_log: dict, solution: str):
    alert_message = (
        f"ALERT: {error_log['timestamp']} [{error_log['level']}] {error_log['message']}\n"
        f"Solution: {solution}"
    )
    logger.info(alert_message)

async def batch_process_logs(batch_interval: int = 60):
    while True:
        await asyncio.sleep(batch_interval)
        batch_logs = []

        # 큐 소비
        while not log_queue.empty():
            log_entry = await log_queue.get()
            batch_logs.append(log_entry)
        if not batch_logs:
            continue

        processed_logs = preprocess_logs(batch_logs)

        error_logs = [log for log in processed_logs if log["level"] == "ERROR"]
        warning_logs = [log for log in processed_logs if log["level"] == "WARNING"]

        for error_log in error_logs:
            solution = await call_llm_api(error_log)
            send_alert(error_log, solution)

        # WARNING 로그는 일단 알림만 보냄
        for warning_log in warning_logs:
            send_alert(warning_log, "warning log")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_log_generator(5))
    asyncio.create_task(batch_process_logs(60))

@app.get("/logs", response_model=List[LogEntry])
def get_logs():
    return preprocess_logs(dummy_logs)

@app.post("/log")
def add_log(log: LogEntry):
    dummy_logs.append(log.dict())
    log_message = f"{log.timestamp} [{log.level}] {log.message}"
    if log.stacktrace:
        log_message += f"\nStacktrace:\n{log.stacktrace}"
    if log.level.upper() == "ERROR":
        logger.error(log_message)
    elif log.level.upper() == "WARNING":
        logger.warning(log_message)
    elif log.level.upper() == "DEBUG":
        logger.debug(log_message)
    else:
        logger.info(log_message)
    return {"message": "Log added", "log": log}

class LogBatch(BaseModel):
    logs: List[LogEntry]

@app.post("/logs/batch")
def add_logs_batch(batch: LogBatch):
    for log in batch.logs:
        dummy_logs.append(log.dict())
        log_message = f"{log.timestamp} [{log.level}] {log.message}"
        if log.stacktrace:
            log_message += f"\nStacktrace:\n{log.stacktrace}"
        if log.level.upper() == "ERROR":
            logger.error(log_message)
        elif log.level.upper() == "WARNING":
            logger.warning(log_message)
        elif log.level.upper() == "DEBUG":
            logger.debug(log_message)
        else:
            logger.info(log_message)
    return {"message": f"{len(batch.logs)} logs added successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)