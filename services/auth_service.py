import hmac
import hashlib
from configs.configs import CLIENT_BOT_SIGNING_SECRET, CLIENT_BOT_SIGNING_VERSION
from helper import string_to_byte
import time


def authenticate_request(request):
    request_body = request.get_data()
    timestamp = request.headers.get('X-Slack-Request-Timestamp')

    # catch older requests
    if abs(time.time() - float(timestamp)) > 60 * 5:
        raise ConnectionError('Authentication failed')

    encoded_header_signature = request.headers.get('X-Slack-Signature').encode()
    base_string = '{}:{}:{}'.format(CLIENT_BOT_SIGNING_VERSION, timestamp, request_body.decode('utf-8'))
    key = string_to_byte(CLIENT_BOT_SIGNING_SECRET)
    message = string_to_byte(base_string)
    hex_hash = hmac.new(key=key, msg=message, digestmod=hashlib.sha256).hexdigest()

    request_signature = CLIENT_BOT_SIGNING_VERSION + '=' + hex_hash

    if not hmac.compare_digest(string_to_byte(request_signature), encoded_header_signature):
        print('Authentication failed - Signature mismatch. Please check the signin secret provided')
        raise ConnectionError('Authentication failed')


def sign_request(timestamp, request_body):
    base_string = '{}:{}:{}'.format(CLIENT_BOT_SIGNING_VERSION, timestamp, request_body.decode('utf-8'))
    key = string_to_byte(CLIENT_BOT_SIGNING_SECRET)
    message = string_to_byte(base_string)
    hex_hash = hmac.new(key=key, msg=message, digestmod=hashlib.sha256).hexdigest()
    return hex_hash
