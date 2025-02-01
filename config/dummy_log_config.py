import random

log_weights = {
    "INFO": 0.5,
    "DEBUG": 0.2,
    "WARNING": 0.2,
    "ERROR": 0.1
}

log_messages = {
    "INFO": [
        "User successfully logged in.",
        "New user registered.",
        "User profile updated successfully.",
        "Email verification completed.",
        "Data successfully synchronized with remote server.",
        "Scheduled job executed successfully.",
        "File uploaded successfully.",
        "Configuration settings updated."
    ],
    "DEBUG": [
        "Starting authentication process for user.",
        "Query executed successfully with 120ms response time.",
        "Cache hit for user session.",
        "API request received, processing...",
        "Session token decoded successfully.",
        "Background task execution started.",
        "Attempting to reconnect to database.",
        "Feature flag enabled: New UI layout active."
    ],
    "WARNING": [
        "User session is about to expire.",
        "Low disk space on server (10% remaining).",
        "High memory usage detected (85% usage).",
        "Deprecated API endpoint was called.",
        "Authentication attempt from unrecognized device.",
        "Service response time is above the threshold.",
        "Rate limit exceeded for IP 192.168.1.100.",
        "SSL certificate will expire in 5 days."
    ],
    "ERROR": [
        "Database connection failed: Timeout after 10 seconds.",
        "Critical service dependency is unavailable.",
        "Payment processing failed due to insufficient funds.",
        "User authentication failed: Invalid credentials.",
        "API request failed with 500 Internal Server Error.",
        "Failed to write to disk: Permission denied.",
        "Email delivery failed: SMTP server not responding.",
        "Uncaught exception in worker thread."
    ]
}

def get_random_log_type() -> str:
    log_types = list(log_weights.keys())
    weights = list(log_weights.values())
    return random.choices(log_types, weights=weights, k=1)[0] 

