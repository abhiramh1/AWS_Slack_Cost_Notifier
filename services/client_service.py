# Functions involving external client calls

import boto3
import requests
import json
from configs.configs import *


def init_aws_client(client_type):
    return boto3.client(client_type)


def init_aws_resource(client_type):
    return boto3.resource(client_type)


def init_aws_client_cost_explorer(client_type, env):
    key = env['aws_key']
    secret = env['aws_secret']
    return boto3.client(client_type)


def send_data_to_client_formatted(content, channel_id):
    url = CLIENT_API_BASE_URL + CLIENT_API_POST_MESSAGE
    api_data = {
        "token": CLIENT_BOT_OAUTH_TOKEN,
        "channel": channel_id,
        "blocks": json.dumps(content)
    }
    response = requests.post(url, data=api_data)
    print("Slack message send with status code: " + str(response.status_code))
    print("Slack message send response: " + str(response.text))


def client_view_actions(view_action, trigger_id, request_data):
    api_url = CLIENT_API_BASE_URL + view_action
    api_data = {
        "token": CLIENT_BOT_OAUTH_TOKEN,
        "trigger_id": trigger_id,
        "view": json.dumps(request_data)
    }
    response = requests.post(api_url, data=api_data)
    print("Slack message send with status code: " + str(response.status_code))
    print("Slack message send response: " + str(response.text))


def client_user_conversations(user, types):
    return_data = {}
    api_url = CLIENT_API_BASE_URL + CLIENT_API_CONVERSATION_LIST + '?types=' + types + '&user=' + user
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + CLIENT_BOT_OAUTH_TOKEN
    }
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    if response_data['ok']:
        return_data = response_data
    return return_data


def client_conversation_name(name):
    return_data = {}
    api_url = CLIENT_API_BASE_URL + CLIENT_API_CONVERSATION_INFO + '?channel=' + name
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + CLIENT_BOT_OAUTH_TOKEN
    }
    response = requests.get(api_url, headers=headers)
    response_data = response.json()
    if response_data['ok']:
        return_data = response_data
    return return_data
