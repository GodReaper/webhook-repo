from logging import Logger
from flask import Blueprint, jsonify, request
from app.extensions import get_events_collection
from datetime import datetime, timedelta
from ..logging_config import get_logger

logger = get_logger('api')

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/events', methods=['GET'])
def get_events():
    """Get events from the last 15 seconds"""
    logger.info("Received request for events")
    
    # Log request details
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    logger.debug(f"Request from IP: {client_ip}, User-Agent: {user_agent}")
    
    try:
        # Calculate timestamp for 15 seconds ago
        fifteen_seconds_ago = datetime.utcnow() - timedelta(seconds=15)
        fifteen_seconds_ago_str = fifteen_seconds_ago.isoformat()
        
        logger.debug(f"Querying events from: {fifteen_seconds_ago_str}")
        
        # Query for events from the last 15 seconds, excluding _id field
        collection = get_events_collection()
        events = list(collection.find({
            'timestamp': {'$gte': fifteen_seconds_ago_str}
        }, {'_id': 0}).sort('timestamp', -1))
        
        logger.info(f"Retrieved {len(events)} events from database")
        logger.debug(f"Events found: {[e.get('action', 'unknown') for e in events]}")
        
        response_data = {'events': events}
        logger.info("Successfully returning events to client")
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error retrieving events: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for API service"""
    logger.debug("API health check requested")
    return jsonify({'status': 'healthy', 'service': 'api'}), 200

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get basic statistics about stored events"""
    logger.info("Received request for event statistics")
    
    try:
        collection = get_events_collection()
        
        # Get total count
        total_events = collection.count_documents({})
        
        # Get events from last 24 hours
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        recent_events = collection.count_documents({
            'timestamp': {'$gte': twenty_four_hours_ago.isoformat()}
        })
        
        # Get events by action type
        pipeline = [
            {'$group': {'_id': '$action', 'count': {'$sum': 1}}}
        ]
        action_stats = list(collection.aggregate(pipeline))
        
        stats = {
            'total_events': total_events,
            'events_last_24h': recent_events,
            'events_by_action': {item['_id']: item['count'] for item in action_stats}
        }
        
        logger.info(f"Statistics: {stats}")
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

