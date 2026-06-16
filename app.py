from flask import Flask, request, jsonify
import json
from lambda_function import handler

app = Flask(__name__)

@app.route('/production/execute', methods=['POST', 'OPTIONS'])
def execute():
    if request.method == 'OPTIONS':
        return ('', 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        })

    try:
        body = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    # Wrap in Lambda-like event so existing handler can be reused
    event = {'body': json.dumps(body), 'requestContext': {'http': {'method': 'POST'}}}
    resp = handler(event, None)
    status = int(resp.get('statusCode', 200))
    headers = resp.get('headers', {}) or {}
    body = resp.get('body', '')

    response = app.response_class(response=body, status=status, mimetype='application/json')
    for k, v in headers.items():
        response.headers[k] = v
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
