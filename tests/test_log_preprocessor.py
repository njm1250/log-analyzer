import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from utils.log_preprocessor import validate_and_clean_log, preprocess_logs


def test_validate_and_clean_log_valid():
    log = {
        "timestamp": " 2025-02-02 10:00:05 ",
        "level": " warning ",
        "message": " disk full ",
        "stacktrace": " trace "
    }
    cleaned = validate_and_clean_log(log)
    assert cleaned == {
        "timestamp": "2025-02-02 10:00:05",
        "level": "WARNING",
        "message": "disk full",
        "stacktrace": "trace"
    }


def test_validate_and_clean_log_missing_field():
    log = {
        "timestamp": "2025-02-02 10:00:05",
        "level": "WARNING"
        # message is missing
    }
    assert validate_and_clean_log(log) is None


def test_validate_and_clean_log_invalid_type():
    log = {
        "timestamp": 123,
        "level": "ERROR",
        "message": "oops"
    }
    assert validate_and_clean_log(log) is None


def test_preprocess_logs_filters_by_level():
    logs = [
        {"timestamp": "t1", "level": "INFO", "message": "info"},
        {"timestamp": "t2", "level": "WARNING", "message": "warn"},
        {"timestamp": "t3", "level": "ERROR", "message": "err"},
        {"timestamp": "t4", "level": "DEBUG", "message": "dbg"},
    ]
    processed = preprocess_logs(logs)
    levels = {log["level"] for log in processed}
    assert levels == {"WARNING", "ERROR"}


def test_preprocess_logs_deduplication():
    logs = [
        {"timestamp": "t1", "level": "WARNING", "message": "dup"},
        {"timestamp": "t2", "level": "warning", "message": "dup", "stacktrace": "trace"},
        {"timestamp": "t3", "level": "ERROR", "message": "unique"},
        {"timestamp": "t4", "level": "ERROR", "message": "unique", "stacktrace": "trace"}
    ]
    processed = preprocess_logs(logs)
    assert len(processed) == 2
    identifiers = {(log["level"], log["message"]) for log in processed}
    assert identifiers == {("WARNING", "dup"), ("ERROR", "unique")}


def test_preprocess_logs_invalid_logs_removed():
    logs = [
        {"timestamp": "t1", "level": "WARNING", "message": "ok"},
        {"timestamp": "t2", "message": "missing level"},
        {"timestamp": 123, "level": "ERROR", "message": "bad type"},
    ]
    processed = preprocess_logs(logs)
    assert processed == [{"timestamp": "t1", "level": "WARNING", "message": "ok", "stacktrace": None}]

