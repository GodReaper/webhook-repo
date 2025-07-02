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

def parse_github_event(payload):
    # Push event
    if 'commits' in payload and 'ref' in payload:
        return {
            'request_id': payload.get('after'),
            'author': payload['pusher']['name'],
            'action': 'PUSH',
            'from_branch': None,
            'to_branch': payload['ref'].split('/')[-1],
            'timestamp': datetime.utcnow().isoformat()
        }
    # Pull request event
    if 'pull_request' in payload:
        pr = payload['pull_request']
        action = 'PULL_REQUEST'
        if payload.get('action') == 'closed' and pr.get('merged'):
            action = 'MERGE'
        return {
            'request_id': str(pr['id']),
            'author': pr['user']['login'],
            'action': action,
            'from_branch': pr['head']['ref'],
            'to_branch': pr['base']['ref'],
            'timestamp': pr['updated_at']
        }
    return None 