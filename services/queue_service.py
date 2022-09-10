from multiprocessing import Process
import requests
import json
from configs.configs import CLIENT_BOT_SIGNING_VERSION
from services.auth_service import sign_request


def init_queue(*args):
    init_queue_process = Process(target=call_dispatch_function, args=args, daemon=True)
    init_queue_process.start()


def call_dispatch_function(payload, request):
    print('inside call_dispatch_function')
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    request_body = json.dumps(payload).encode('utf-8')
    hex_hash = sign_request(timestamp, request_body)
    base_url = request.url_root
    request_header = {
        'X-Slack-Request-Timestamp': request.headers.get('X-Slack-Request-Timestamp'),
        'X-Slack-Signature': CLIENT_BOT_SIGNING_VERSION + '=' + hex_hash,
        'Content-Type': 'application/json'
    }
    url = base_url + 'process-cost-details/from_api_request'
    response = requests.post(url, headers=request_header, data=json.dumps(payload))
    print("call_dispatch_function ended with status code: " + str(response.status_code))
    print("call_dispatch_function ended with content :" + str(response.text))
