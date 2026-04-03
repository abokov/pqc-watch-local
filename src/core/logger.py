import logging
import json
import time
from .config_loader import config

class JSONFormatter(logging.Formatter):
    """Custom formatter to output JSON logs."""
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

def setup_logger():
    """Initializes the logger based on config settings."""
    log_level = config.get("logging.level", "INFO").upper()
    log_file = config.get("logging.file_path", "pqc_watch.log")
    
    logger = logging.getLogger("pqc_watch")
    logger.setLevel(getattr(logging, log_level))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # JSON File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    # Stream Handler (Standard Output)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(JSONFormatter())
    logger.addHandler(stream_handler)
    
    return logger

# Global logger instance
logger = setup_logger()
