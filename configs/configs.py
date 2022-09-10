import os

SYSTEM_PORT = 8000

'''AWS Details'''
AWS_SERVER_PUBLIC_KEY = ''
AWS_SERVER_SECRET_KEY = ''
S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_USER_DETAILS')

'''Client is SLACK'''
CLIENT_API_BASE_URL = 'https://slack.com/api/'
CLIENT_API_VIEW_OPEN = 'views.open'
CLIENT_API_VIEW_UPDATE = 'views.update'
CLIENT_API_VIEW_PUSH = 'views.push'
CLIENT_API_POST_MESSAGE = 'chat.postMessage'
CLIENT_API_CONVERSATION_LIST = 'users.conversations'
CLIENT_API_CONVERSATION_INFO = 'conversations.info'
CLIENT_BOT_OAUTH_TOKEN = os.environ.get('CLIENT_BOT_OAUTH_TOKEN')
CLIENT_BOT_SIGNING_SECRET = os.environ.get('CLIENT_BOT_SIGNING_SECRET')
CLIENT_BOT_SIGNING_VERSION = 'v0'  # default set as v0 by slack

'''Environments'''

SERVICE_KEY_AWS = 'aws'
SERVICE_KEY_GITHUB = 'github'
SERVICE_KEY_CONFLUENCE = 'confluence'

SERVICE_AWS_EMOJI = ":awslogo:"
SERVICE_AWS_GITHUB = ":githublogo:"

SERVICE_AWS_LABEL_NON_PROD = "NON-PROD"
SERVICE_AWS_KEY_NON_PROD = "non-prod"
SERVICE_AWS_REGEX_NON_PROD = "Non Production"

SERVICE_AWS_LABEL_PROD = "PROD"
SERVICE_AWS_KEY_PROD = "prod"
SERVICE_AWS_REGEX_PROD = "Production"

SERVICE_AWS_LABEL_DEV = "DEV"
SERVICE_AWS_KEY_DEV = "dev"
SERVICE_AWS_REGEX_DEV = "Development"

SERVICE_AWS_LABEL_SHARED = "SHARED"
SERVICE_AWS_KEY_SHARED = "shared"
SERVICE_AWS_REGEX_SHARED = "Shared"

ALL_SERVICES_DETAILS = [
    {
        "key": SERVICE_KEY_AWS,
        "data": {
            SERVICE_AWS_KEY_NON_PROD: {
                "label": SERVICE_AWS_LABEL_NON_PROD,
                "emoji": SERVICE_AWS_EMOJI,
                "env": SERVICE_AWS_KEY_NON_PROD,
                "regex": SERVICE_AWS_REGEX_NON_PROD
            },
            SERVICE_AWS_KEY_PROD: {
                "label": SERVICE_AWS_LABEL_PROD,
                "emoji": SERVICE_AWS_EMOJI,
                "env": SERVICE_AWS_KEY_PROD,
                "regex": SERVICE_AWS_REGEX_PROD
            },
            SERVICE_AWS_KEY_DEV: {
                "label": SERVICE_AWS_LABEL_DEV,
                "emoji": SERVICE_AWS_EMOJI,
                "env": SERVICE_AWS_KEY_DEV,
                "regex": SERVICE_AWS_REGEX_DEV
            },
            SERVICE_AWS_KEY_SHARED: {
                "label": SERVICE_AWS_LABEL_SHARED,
                "emoji": SERVICE_AWS_EMOJI,
                "env": SERVICE_AWS_KEY_SHARED,
                "regex": SERVICE_AWS_REGEX_SHARED
            },
        }
    },
    {
        "key": SERVICE_KEY_GITHUB,
        "data": {}
    },
    {
        "key": SERVICE_KEY_CONFLUENCE,
        "data": {}
    }
]
