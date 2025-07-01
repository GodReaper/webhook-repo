from datetime import datetime

def parse_event(data):
    """
    Parse and validate incoming webhook data to match the MongoDB schema.
    Returns a dict ready for MongoDB insertion or None if invalid.
    """
    required_fields = ['request_id', 'author', 'action', 'timestamp']
    for field in required_fields:
        if field not in data:
            return None
    event = {
        'request_id': data['request_id'],
        'author': data['author'],
        'action': data['action'],
        'from_branch': data.get('from_branch'),
        'to_branch': data.get('to_branch'),
        'timestamp': data['timestamp'] if isinstance(data['timestamp'], str) else datetime.utcnow().isoformat()
    }
    return event 