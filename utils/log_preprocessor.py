from typing import List, Dict, Optional

# 전처리 시 유지할 로그 레벨
ALLOWED_LOG_LEVELS = {"WARNING", "ERROR"}

def validate_and_clean_log(log: dict) -> Optional[Dict]:
    required_fields = ['timestamp', 'level', 'message']
    for field in required_fields:
        if field not in log or not isinstance(log[field], str):
            return None

    cleaned_log = {
        "timestamp": log["timestamp"].strip(),
        "level": log["level"].strip().upper(),
        "message": log["message"].strip()
    }

    if "stacktrace" in log and isinstance(log["stacktrace"], str):
        cleaned_log["stacktrace"] = log["stacktrace"].strip()
    else:
        cleaned_log["stacktrace"] = None

    return cleaned_log

def preprocess_logs(logs: List[Dict]) -> List[Dict]:
    valid_logs = []
    for log in logs:
        cleaned = validate_and_clean_log(log)
        if not cleaned:
            continue
        if cleaned["level"] not in ALLOWED_LOG_LEVELS:
            continue
        valid_logs.append(cleaned)

    seen = set()
    deduped_logs = []
    for log in valid_logs:
        identifier = (log["level"], log["message"])
        if identifier not in seen:
            seen.add(identifier)
            deduped_logs.append(log)
    return deduped_logs

# 테스트
if __name__ == '__main__':
    sample_logs = [
        {"timestamp": "2025-02-02 10:00:00", "level": "INFO", "message": "시스템 시작."},
        {"timestamp": "2025-02-02 10:00:05", "level": "WARNING", "message": "디스크 용량 부족."},
        {"timestamp": "2025-02-02 10:00:05", "level": "WARNING", "message": "디스크 용량 부족.", "stacktrace": "Traceback (most recent call last): ..."},
        {"timestamp": "2025-02-02 10:00:10", "level": "ERROR", "message": "연결 실패.", "stacktrace": "Traceback (most recent call last): ..."},
        {"timestamp": "2025-02-02 10:00:15", "level": "DEBUG", "message": "디버그 정보."},
    ]

    processed_logs = preprocess_logs(sample_logs)
    for log in processed_logs:
        print(log)
