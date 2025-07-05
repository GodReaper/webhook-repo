from datetime import datetime
from .logging_config import get_logger

logger = get_logger('models')

def parse_event(data):
    """
    Parse and validate incoming webhook data to match the MongoDB schema.
    Returns a dict ready for MongoDB insertion or None if invalid.
    """
    logger.debug(f"Parsing event data: {data}")
    
    required_fields = ['request_id', 'author', 'action', 'timestamp']
    
    # Check for required fields
    for field in required_fields:
        if field not in data:
            logger.warning(f"Missing required field: {field}")
            logger.debug(f"Available fields: {list(data.keys())}")
            return None
    
    event = {
        'request_id': data['request_id'],
        'author': data['author'],
        'action': data['action'],
        'from_branch': data.get('from_branch'),
        'to_branch': data.get('to_branch'),
        'timestamp': data['timestamp'] if isinstance(data['timestamp'], str) else datetime.utcnow().isoformat()
    }
    
    logger.info(f"Successfully parsed event: {event['action']} by {event['author']}")
    logger.debug(f"Parsed event details: {event}")
    
    return event

def parse_github_event(payload):
    """Parse GitHub webhook payload into our event format"""
    logger.debug(f"Parsing GitHub webhook payload: {payload}")
    
    # Push event
    if 'commits' in payload and 'ref' in payload:
        logger.info("Processing GitHub push event")
        
        event = {
            'request_id': payload.get('after'),
            'author': payload['pusher']['name'],
            'action': 'PUSH',
            'from_branch': None,
            'to_branch': payload['ref'].split('/')[-1],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Parsed push event: {event['author']} pushed to {event['to_branch']}")
        return event
    
    # Pull request event
    if 'pull_request' in payload:
        logger.info("Processing GitHub pull request event")
        
        pr = payload['pull_request']
        action = 'PULL_REQUEST'
        
        if payload.get('action') == 'closed' and pr.get('merged'):
            action = 'MERGE'
            logger.info("Pull request was merged")
        
        event = {
            'request_id': str(pr['id']),
            'author': pr['user']['login'],
            'action': action,
            'from_branch': pr['head']['ref'],
            'to_branch': pr['base']['ref'],
            'timestamp': pr['updated_at']
        }
        
        logger.info(f"Parsed {action.lower()} event: {event['author']} from {event['from_branch']} to {event['to_branch']}")
        return event
    
    logger.warning(f"Unknown GitHub event type: {payload.get('ref', 'no ref')} - {list(payload.keys())}")
    return None 