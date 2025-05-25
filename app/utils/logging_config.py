import logging
import json
import time
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'request_id'):
            log_record["request_id"] = record.request_id
            
        if hasattr(record, 'user_id'):
            log_record["user_id"] = record.user_id
            
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logging(service_name):
    """Configure logging for the application"""
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    if logger.handlers:
        logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)
    
    # File handler - daily rotating log file
    today = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f"logs/{service_name}_{today}.log")
    file_handler.setFormatter(CustomFormatter())
    logger.addHandler(file_handler)
    
    return logger