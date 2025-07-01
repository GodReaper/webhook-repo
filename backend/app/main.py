from flask import Flask, jsonify
from .routes import register_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
register_routes(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 