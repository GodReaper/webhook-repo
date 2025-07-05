import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging():
    """
    Configure logging for the application with different levels and handlers
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler (INFO level and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs (DEBUG level and above)
    all_logs_file = os.path.join(log_dir, 'app.log')
    file_handler = logging.handlers.RotatingFileHandler(
        all_logs_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # Error file handler (ERROR level and above)
    error_logs_file = os.path.join(log_dir, 'errors.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_logs_file, maxBytes=10*1024*1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # Webhook specific logger
    webhook_logger = logging.getLogger('webhook')
    webhook_logger.setLevel(logging.INFO)
    
    # API specific logger
    api_logger = logging.getLogger('api')
    api_logger.setLevel(logging.INFO)
    
    # Database specific logger
    db_logger = logging.getLogger('database')
    db_logger.setLevel(logging.INFO)
    
    # Model specific logger
    model_logger = logging.getLogger('models')
    model_logger.setLevel(logging.INFO)
    
    # Log startup message
    root_logger.info("Logging system initialized")
    root_logger.info(f"Log files directory: {log_dir}")
    
    return root_logger

def get_logger(name):
    """
    Get a logger instance with the specified name
    """
    return logging.getLogger(name) 