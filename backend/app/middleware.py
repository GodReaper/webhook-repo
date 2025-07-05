import time
from flask import request, g
from .logging_config import get_logger

logger = get_logger('middleware')

def log_request_start():
    """Log the start of each request"""
    g.start_time = time.time()
    
    # Log request details
    logger.info(f"Request started: {request.method} {request.path}")
    logger.debug(f"Request details - IP: {request.remote_addr}, "
                f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}, "
                f"Content-Type: {request.headers.get('Content-Type', 'None')}")

def log_request_end(response):
    """Log the end of each request with timing information"""
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        logger.info(f"Request completed: {request.method} {request.path} - "
                   f"Status: {response.status_code}, Duration: {duration:.3f}s")
    else:
        logger.info(f"Request completed: {request.method} {request.path} - "
                   f"Status: {response.status_code}")
    
    return response

def log_request_error(error):
    """Log request errors"""
    logger.error(f"Request error: {request.method} {request.path} - "
                f"Error: {str(error)}")
    return error 