import os
from flask import Blueprint, jsonify, request
from app.extensions import get_events_collection
from ..models import parse_github_event  

WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

webhook_bp = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook_bp.route('/receiver', methods=['POST'])
def webhook():
    payload = request.json
    if not payload:
        return jsonify({'error': 'Invalid or missing JSON'}), 400
    event = parse_github_event(payload)
    if not event:
        return jsonify({'error': 'Invalid event'}), 400
    get_events_collection().insert_one(event)
    return jsonify({'status': 'ok'}), 200
