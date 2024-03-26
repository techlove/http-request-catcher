from datetime import datetime
from flask import Flask, request, jsonify, json
from os import environ
from htmltemplate import Template
# import json
app = Flask('HTTP Request Catcher')

last_request = None
last_requests = []

template = Template('''
<!DOCTYPE html>
<html>
<head>
    <title>HTTP Request Catcher</title>
</head>
<body>
    <h1>HTTP Request Catcher</h1>
    <button onclick="clearRequests()">Clear Requests</button>
    <pre node="con:requests"></pre>
    <script>
        function clearRequests() {
            fetch('/__clear_requests__', {
                method: 'DELETE'
            }).then(() => {
                window.location.reload();
            });
        }
    </script>
</body>
</html>
''')

def render_requests(node, requests):
    indent = 2
    separators = (', ', ': ')
    json.dumps(requests, indent=indent, separators=separators)
    node.requests.text = json.dumps(requests)


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204

@app.route('/__clear_requests__', methods=['DELETE'])
def clear_requests():
    global last_requests
    last_requests = []
    return '', 204

@app.route('/__last_requests__', methods=['GET'])
def get_last_requests():
    return template.render(render_requests, last_requests), 200


@app.route('/__last_request__', methods=['GET'])
def get_last_request():
    return jsonify(last_request), 200


@app.route('/', defaults={'path': ''}, methods=['PUT', 'POST', 'GET', 'HEAD', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['PUT', 'POST', 'GET', 'HEAD', 'DELETE', 'PATCH', 'OPTIONS'])
def catch(path):
    global last_request

    last_request = {
        'method': request.method,
        'data': request.data.decode('utf-8'),
        'headers': dict(request.headers),
        'url': request.url,
        'time': datetime.now().isoformat(),
    }

    last_requests.append(last_request)

    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
