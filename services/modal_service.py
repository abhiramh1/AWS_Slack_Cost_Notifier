# Methods for miscellaneous functions and custom edit modals

from configs.modal_config import *
import json
from helper import format_currency_digits, round_float
from services.storage_service import is_file_available_in_s3
from services.client_service import client_user_conversations
from services.cost_service import get_cost_tags


def build_modal_alert_listing(action_type, action_label, button_label='Submit'):
    return {
        "type": "modal",
        "private_metadata": action_type,
        "callback_id": action_type,
        "title": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": MODAL_HEADER
        },
        "blocks": [build_block_for_alert_drop_down(action_label)],
        "submit": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": button_label
        },
        "close": GO_BACK_MODAL
    }


def build_modal_alert_listing_for_update(action_type, action_label, button_label='Submit'):
    return {
        "type": "modal",
        "private_metadata": action_type,
        "callback_id": action_type,
        "title": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": MODAL_HEADER
        },
        "blocks": [
            build_block_for_alert_drop_down(action_label)
        ],
        "submit": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": button_label
        },
        "close": GO_BACK_MODAL
    }


def build_update_modal_shared(request):
    return {
        "type": "modal",
        "private_metadata": "update_project_shared",
        "callback_id": request['report_id'],
        "title": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": MODAL_HEADER
        },
        "blocks": [
            {
                "type": MODAL_TYPE_INPUT,
                "block_id": MODAL_VALUE_ALERT_NAME,
                "element": {
                    "type": MODAL_INPUT_TYPE_PLAIN_TEXT,
                    "action_id": MODAL_VALUE_ALERT_NAME,
                    "initial_value": request['alert_name'],
                    "placeholder": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "Enter a name for your notification"
                    }
                },
                "label": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Enter Alert name or description"
                }
            },
            {
                "block_id": MODAL_VALUE_PROJECT_TAG,
                "type": MODAL_TYPE_INPUT,
                "label": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Select the Project Tag"
                },
                "element": {
                    "action_id": MODAL_VALUE_PROJECT_TAG,
                    "initial_option": {
                        "value": request['project_tag'],
                        "text": {
                            "type": MODAL_TYPE_PLAIN_TEXT,
                            "text": request['project_tag']
                        }
                    },
                    "type": MODAL_INPUT_TYPE_EXTERNAL_SELECT,
                    "min_query_length": 0,
                    "placeholder": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "Pick an existing project tag available in shared account"
                    }
                }
            },
            {
                "type": MODAL_TYPE_INPUT,
                "block_id": MODAL_VALUE_BUDGET_LIMIT,
                "element": {
                    "type": MODAL_INPUT_TYPE_PLAIN_TEXT,
                    "action_id": MODAL_VALUE_BUDGET_LIMIT,
                    "initial_value": request['budget_limit'],
                    "placeholder": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "e.g. 10000"
                }
                },
                "label": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Budget Limit (in USD $)"
                }
            },
            {
                "type": MODAL_TYPE_INPUT,
                "block_id": MODAL_VALUE_BUDGET_THRESHOLD,
                "element": {
                    "type": MODAL_INPUT_TYPE_PLAIN_TEXT,
                    "action_id": MODAL_VALUE_BUDGET_THRESHOLD,
                    "initial_value": request['budget_threshold'],
                    "placeholder": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "e.g. 90"
                    }
                },
                "label": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Budget Threshold (in %)"
                }
            },
            {
                "type": MODAL_TYPE_INPUT,
                "block_id": MODAL_VALUE_REPORT_SCHEDULE,
                "element": {
                    "type": MODAL_INPUT_TYPE_RADIO_BUTTON,
                    "initial_option": {
                        "value": request['report_schedule'],
                        "text": {
                            "type": MODAL_TYPE_PLAIN_TEXT,
                            "text": REPORT_SCHEDULE[request['report_schedule']]
                        }
                    },
                    "options": SCHEDULE_OPTIONS,
                    "action_id": MODAL_VALUE_REPORT_SCHEDULE
                },
                "label": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Scheduling Frequency"
                }
            },
            {
                "block_id": MODAL_VALUE_CHANNEL_ID,
                "type": MODAL_TYPE_INPUT,
                "label": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Select a channel to send the notification"
                },
                "element": {
                    "action_id": MODAL_VALUE_CHANNEL_ID,
                    "initial_option": {
                        "value": request['channel_id'],
                        "text": {
                            "type": MODAL_TYPE_PLAIN_TEXT,
                            "text": request['channel_name']
                        }
                    },
                    "type": MODAL_INPUT_TYPE_EXTERNAL_SELECT,
                    "min_query_length": 0,
                    "placeholder": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "Pick an channel"
                    }
                }
            },
            # {
            #     "block_id": MODAL_VALUE_CHANNEL_ID,
            #     "type": MODAL_TYPE_INPUT,
            #     "label": {
            #         "type": MODAL_TYPE_PLAIN_TEXT,
            #         "text": "Select a channel to send the notification"
            #     },
            #     "element": {
            #         "action_id": MODAL_VALUE_CHANNEL_ID,
            #         "type": MODAL_INPUT_TYPE_CONVERSATION_SELECT,
            #         "initial_conversation": request['channel_id'],
            #         "filter": {
            #             "include": [
            #                 "private",
            #                 "public"
            #             ]
            #         }
            #     }
            # },
            PRIVATE_CHANNEL_INFO_MODAL_SECTION,
            VIEW_NOW_MODAL
        ],
        "submit": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "Update"
        },
        "close": GO_BACK_MODAL
}


def build_block_for_alert_drop_down(action_label):
    return {
        "block_id": MODAL_VALUE_ALERT_LIST,
        "type": MODAL_TYPE_INPUT,
        "label": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "Select the notification you want to " + action_label
        },
        "element": {
            "action_id": MODAL_VALUE_ALERT_LIST,
            "type": MODAL_INPUT_TYPE_EXTERNAL_SELECT,
            "min_query_length": 0
        }
    }


def build_generate_completion_modal(text):
    return {
        "type": "modal",
        "private_metadata": "on_completion_report",
        "title": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": MODAL_HEADER,
        },
        "close": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "Home",
        },
        "blocks": [
            {
                "type": MODAL_TYPE_SECTION,
                "text": {
                    "type": MODAL_TYPE_MRK_DWN,
                    "text": text
                }
            }
        ]
    }


def validation_error(block_id):
    return {
        "response_action": "errors",
        "errors": {
            block_id: "Only numeric values are allowed here"
        }
    }


def view_actions(action, payload):
    return {
        "response_action": action,
        "view": json.dumps(payload)
    }


def build_plain_message(content):
    return [
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_MRK_DWN,
                "text": content
            }
        }
    ]


def build_alert_block_updated(block_elements):
    cost_details_block = build_cost_details_block(block_elements['services'])
    return build_modal_notification_to_client(block_elements, cost_details_block)


def build_cost_details_block(cost_details):
    data_block = []
    for key, elements in cost_details.items():
        for inner_key, inner_elements in elements.items():
            cost_details_block = {
                "type": MODAL_TYPE_SECTION,
                "fields": []
            }
            up_or_down_trend = CLIENT_EMOJI_TREND_UP if inner_elements['is_trend_up'] else CLIENT_EMOJI_TREND_DOWN
            total_usage_trend = "+" if inner_elements['is_trend_up'] else "-"
            print(inner_elements['label'])
            cost_details_block['fields'].append({
                "type": MODAL_TYPE_MRK_DWN,
                "text": inner_elements['emoji'] + " *" + inner_elements['label'] + "*"
            }
            )
            cost_details_block['fields'].append({
                "type": MODAL_TYPE_MRK_DWN,
                "text": up_or_down_trend + " $" + str(round_float(inner_elements['total_cost'])) + " (" + total_usage_trend + str(
                    inner_elements['trend_usage_percentage']) + "%)"
            })
            data_block.append(cost_details_block)
    return data_block


def load_alert_list_for_dropdown(json_decoded_payload):
    user_id = json_decoded_payload['user']['id']
    user_alert_details_file = user_id + '.json'
    details = is_file_available_in_s3(user_alert_details_file)
    external_menu_options = []
    if details:
        for alert in details:
            if alert['active']:
                data = {
                    "text": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": alert['alert_name']
                    },
                    "value": alert['report_id']
                }
                external_menu_options.append(data)
    return external_menu_options


def load_channel_list_for_dropdown(json_decoded_payload):
    user_id = json_decoded_payload['user']['id']
    user_name = json_decoded_payload['user']['username']
    search_string = json_decoded_payload['value']
    conversation_type = 'public_channel,private_channel'
    conversation_data = client_user_conversations(user_id, conversation_type)
    print("Conversation details from Client: " + str(conversation_data))
    data_list = [{
        "text": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": CLIENT_EMOJI_USER_CHANNEL + '\t' + user_name + ' (you)'
        },
        "value": user_id
    }]
    if conversation_data:
        channel_list = conversation_data['channels']
        for channel in channel_list:
            channel_icon = CLIENT_EMOJI_PRIVATE_CHANNEL if channel['is_private'] else CLIENT_EMOJI_PUBLIC_CHANNEL
            if not search_string or (search_string and search_string in channel['name']):
                channel_data = {
                    "text": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": channel_icon + '\t' + channel['name']
                    },
                    "value": channel['id']
                }
                data_list.append(channel_data)
    return data_list


def load_project_tag_details(search_string):
    # Project key if hardcoded as the initial requirement. This shall evolve into much wider Tags
    aws_tag_details = get_cost_tags(key='Project', search_string=search_string)
    print("Tag details from AWS: " + str(aws_tag_details))
    tag_details = []
    project_tags = aws_tag_details['Tags']
    for tag_name in project_tags:
        if tag_name:
            tag_details.append(
                {
                    "text": {
                        "type": "plain_text",
                        "text": tag_name
                    },
                    "value": tag_name
                }
            )
    return tag_details


def build_modal_notification_to_client(block_elements, cost_details_block):
    breached_emoji = CLIENT_EMOJI_IF_BREACHED if block_elements['is_threshold_breached'] else CLIENT_EMOJI_IF_NOT_BREACHED
    up_or_down_trend = CLIENT_EMOJI_TREND_UP if block_elements['is_trend_up'] else CLIENT_EMOJI_TREND_DOWN
    total_usage_trend = "+" if block_elements['is_trend_up'] else "-"
    header_block = [
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_MRK_DWN,
                "text": REPORT_SCHEDULE[block_elements['report_schedule']] + " report for *" + block_elements['alert_name'] +
                        "* from " + block_elements['start_date'] + " to " + block_elements['end_date']
            }
        },
        {
            "type": MODAL_TYPE_DIVIDER
        }
    ]
    for data_block in cost_details_block:
        header_block.append(data_block)
    header_block.append({
        "type": MODAL_TYPE_DIVIDER
    })
    header_block.append({
        "type": MODAL_TYPE_SECTION,
        "fields": [
            {
                "type": MODAL_TYPE_MRK_DWN,
                "text": "*Total*"
            },
            {
                "type": MODAL_TYPE_MRK_DWN,
                "text": up_or_down_trend + " $" + str(
                    format_currency_digits(block_elements['total_service_usage'])) + " (" + total_usage_trend + str(
                    block_elements['trend_usage_percentage']) + "%)"
            },
            {
                "type": MODAL_TYPE_MRK_DWN,
                "text": "*Budget*"
            },
            {
                "type": MODAL_TYPE_MRK_DWN,
                "text": breached_emoji + " $" + str(block_elements['budget_limit']) + " (" + str(
                    int(float(block_elements['trend_budget_utilised']))) + "%)"
            }
        ]
    })
    return header_block
