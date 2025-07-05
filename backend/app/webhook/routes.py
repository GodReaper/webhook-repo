import os
from flask import Blueprint, jsonify, request
from app.extensions import get_events_collection
from ..models import parse_github_event
from ..logging_config import get_logger

logger = get_logger('webhook')

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook_bp.route('/receiver', methods=['POST'])
def webhook():
    """Handle incoming GitHub webhook events"""
    logger.info("Received webhook request")
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request URL: {request.url}")
    
    # Log client information
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    logger.info(f"Webhook request from IP: {client_ip}, User-Agent: {user_agent}")
    
    # Validate request content type
    if not request.is_json:
        logger.warning("Invalid request: Content-Type is not application/json")
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    # Get JSON payload
    try:
        payload = request.json
        logger.debug(f"Received payload keys: {list(payload.keys()) if payload else 'None'}")
    except Exception as e:
        logger.error(f"Failed to parse JSON payload: {str(e)}")
        return jsonify({'error': 'Invalid JSON payload'}), 400
    
    if not payload:
        logger.warning("Empty or missing JSON payload")
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    
    # Log GitHub event type if available
    github_event = request.headers.get('X-GitHub-Event', 'Unknown')
    logger.info(f"GitHub event type: {github_event}")
    
    # Parse the event
    try:
        event = parse_github_event(payload)
        if not event:
            logger.warning(f"Failed to parse GitHub event: {github_event}")
            return jsonify({'error': 'Invalid event'}), 400
        
        logger.info(f"Successfully parsed event: {event['action']} by {event['author']}")
        
    except Exception as e:
        logger.error(f"Exception while parsing event: {str(e)}")
        return jsonify({'error': 'Error processing event'}), 500
    
    # Store event in database
    try:
        collection = get_events_collection()
        result = collection.insert_one(event)
        logger.info(f"Event stored in database with ID: {result.inserted_id}")
        
    except Exception as e:
        logger.error(f"Failed to store event in database: {str(e)}")
        return jsonify({'error': 'Database error'}), 500
    
    logger.info("Webhook processed successfully")
    return jsonify({'status': 'ok', 'event_id': str(result.inserted_id)}), 200

@webhook_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for webhook service"""
    logger.debug("Health check requested")
    return jsonify({'status': 'healthy', 'service': 'webhook'}), 200
