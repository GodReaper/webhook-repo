from flask import Blueprint, jsonify
from app.extensions import get_events_collection

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/events', methods=['GET'])
def get_events():
    events = list(get_events_collection().find().sort('timestamp', -1).limit(20))
    for e in events:
        e['_id'] = str(e['_id'])
    return jsonify({'events': events})
