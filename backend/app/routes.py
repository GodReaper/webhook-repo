import os
from flask import request, jsonify
from .db import get_events_collection
from .models import parse_event
from datetime import datetime

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')


def register_routes(app):
    @app.route('/webhook', methods=['POST'])
    def webhook():
        # Auth check
        # secret = request.headers.get('X-Webhook-Secret')
        # if not secret or secret != WEBHOOK_SECRET:
        #     return jsonify({'error': 'Unauthorized'}), 401
        payload = request.json
        # Parse event type and normalize
        event = parse_github_event(payload)
        if not event:
            return jsonify({'error': 'Invalid event'}), 400
        get_events_collection().insert_one(event)
        return jsonify({'status': 'ok'})

    @app.route('/api/events', methods=['GET'])
    def get_events():
        # Return latest 20 events, sorted by timestamp desc
        events = list(get_events_collection().find().sort('timestamp', -1).limit(20))
        for e in events:
            e['_id'] = str(e['_id'])
        return jsonify({'events': events})


def parse_github_event(payload):
    """
    Normalize GitHub webhook payloads to our schema.
    Handles push, pull_request, and infers merge from pull_request.closed+merged.
    """
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
        # Infer merge
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