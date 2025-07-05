from logging import Logger
from flask import Blueprint, jsonify
from app.extensions import get_events_collection

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/events', methods=['GET'])
def get_events():
    events = list(get_events_collection().find().sort('timestamp', -1).limit(20))

    print(type(events))
    return jsonify({'events': events})

