from configs.constants import *

''' Modal Constants - Inner modal component '''

GO_BACK_MODAL = {
    "type": MODAL_TYPE_PLAIN_TEXT,
    "text": "Back"
}

HEADER_MODAL = {
    "type": MODAL_TYPE_HEADER,
    "text": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Select Account Type"
    }
}

ALERT_NAME_MODAL = {
    "type": MODAL_TYPE_INPUT,
    "block_id": MODAL_VALUE_ALERT_NAME,
    "element": {
        "type": MODAL_INPUT_TYPE_PLAIN_TEXT,
        "action_id": MODAL_VALUE_ALERT_NAME,
        "placeholder": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "e.g. My Daily Project Notification"
        }
    },
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Enter a name for your notification"
    }
}

BUDGET_LIMIT_MODAL = {
    "type": MODAL_TYPE_INPUT,
    "block_id": MODAL_VALUE_BUDGET_LIMIT,
    "element": {
        "type": MODAL_INPUT_TYPE_PLAIN_TEXT,
        "action_id": MODAL_VALUE_BUDGET_LIMIT,
        "placeholder": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "e.g. 10000"
        }
    },
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Budget Limit (in USD $)"
    }
}

BUDGET_THRESHOLD_MODAL = {
    "type": MODAL_TYPE_INPUT,
    "block_id": MODAL_VALUE_BUDGET_THRESHOLD,
    "element": {
        "type": MODAL_INPUT_TYPE_PLAIN_TEXT,
        "action_id": MODAL_VALUE_BUDGET_THRESHOLD,
        "placeholder": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "e.g. 90"
        }
    },
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Budget Threshold (in %)"
    }
}

SCHEDULE_OPTIONS = [
    {
        "text": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": REPORT_SCHEDULE[REPORT_TYPE_DAILY]
        },
        "value": REPORT_TYPE_DAILY
    },
    {
        "text": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": REPORT_SCHEDULE[REPORT_TYPE_WEEKLY]
        },
        "value": REPORT_TYPE_WEEKLY
    },
    {
        "text": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": REPORT_SCHEDULE[REPORT_TYPE_MONTHLY]
        },
        "value": REPORT_TYPE_MONTHLY
    }
]

REPORT_SCHEDULE_MODAL = {
    "type": MODAL_TYPE_INPUT,
    "block_id": MODAL_VALUE_REPORT_SCHEDULE,
    "element": {
        "type": MODAL_INPUT_TYPE_RADIO_BUTTON,
        "initial_option": {
            "value": REPORT_TYPE_MONTHLY,
            "text": {
                "type": MODAL_TYPE_PLAIN_TEXT,
                "text": REPORT_SCHEDULE[REPORT_TYPE_MONTHLY]
            }
        },
        "options": SCHEDULE_OPTIONS,
        "action_id": MODAL_VALUE_REPORT_SCHEDULE
    },
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Scheduling Frequency"
    }
}

CHANNEL_SELECT_MODAL = {
    "block_id": MODAL_VALUE_CHANNEL_ID,
    "type": MODAL_TYPE_INPUT,
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Select a channel to send the notification"
    },
    "element": {
        "action_id": MODAL_VALUE_CHANNEL_ID,
        "type": MODAL_INPUT_TYPE_EXTERNAL_SELECT,
        "min_query_length": 0,
        "placeholder": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "Pick a channel"
        }
    }
}

PRIVATE_CHANNEL_INFO_MODAL_SECTION = {
     "type": MODAL_TYPE_CONTEXT,
     "elements": [
         {
             "type": MODAL_TYPE_MRK_DWN,
             "text": "Private channels where the Bot has been invited will be listed here"
         }
     ]
 }

# CHANNEL_SELECT_MODAL = {
#     "block_id": MODAL_VALUE_CHANNEL_ID,
#     "type": MODAL_TYPE_INPUT,
#     "label": {
#         "type": MODAL_TYPE_PLAIN_TEXT,
#         "text": "Select a channel to send the notification"
#     },
#     "element": {
#         "action_id": MODAL_VALUE_CHANNEL_ID,
#         "type": MODAL_INPUT_TYPE_CONVERSATION_SELECT,
#         "placeholder": {
#             "type": MODAL_TYPE_PLAIN_TEXT,
#             "text": "Pick a channel"
#         },
#         "filter": {
#             "include": [
#                 "private",
#                 "public"
#             ]
#         },
#     }
# }

VIEW_NOW_MODAL = {
    "type": MODAL_TYPE_INPUT,
    "block_id": MODAL_VALUE_SEND_NOW,
    "optional": True,
    "element": {
        "type": MODAL_INPUT_TYPE_CHECKBOX,
        "options": [
            {
                "text": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Check this if you want to generate the report now"
                },
                "value": "value-0"
            }
        ],
        "action_id": MODAL_VALUE_SEND_NOW
    },
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "View Report"
    }
}

BLOCK_ALERT_LIST = {
    "block_id": MODAL_VALUE_ALERT_LIST,
    "type": MODAL_TYPE_INPUT,
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Select an Alert Name/Description"
    },
    "element": {
        "action_id": MODAL_VALUE_ALERT_LIST,
        "type": MODAL_INPUT_TYPE_EXTERNAL_SELECT,
        "min_query_length": 0
    }
}

PROJECT_TAG_MODAL = {
    "block_id": MODAL_VALUE_PROJECT_TAG,
    "type": MODAL_TYPE_INPUT,
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Select the Project Tag"
    },
    "element": {
        "action_id": MODAL_VALUE_PROJECT_TAG,
        "type": MODAL_INPUT_TYPE_EXTERNAL_SELECT,
        "min_query_length": 0,
        "placeholder": {
            "type": MODAL_TYPE_PLAIN_TEXT,
            "text": "Pick an existing project tag available in shared account"
        }
    }
}

# Visibility modal only for testing purpose TODO - To be verified
NOTIFICATION_VISIBILITY_MODAL = {
    "type": MODAL_TYPE_INPUT,
    "block_id": "only_me",
    "element": {
        "type": "radio_buttons",
        "initial_option": {
            "value": "1",
            "text": {
                "type": MODAL_TYPE_PLAIN_TEXT,
                "text": "Only me"
            }
        },
        "options": [
            {
                "text": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Only me"
                },
                "value": "1"
            },
            {
                "text": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Everyone in the channel"
                },
                "value": "2"
            }
        ],
        "action_id": "only_me"
    },
    "label": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Report visibility"
    }
}

''' Modal Constants - Popup builder '''

MODAL_BUILDER_DATA_FAST = {
    "type": "modal",
    "private_metadata": MODAL_VALUE_PROJECT_FAST,
    "callback_id": MODAL_VALUE_PROJECT_FAST,
    "title": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": MODAL_HEADER
    },
    "submit": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Submit"
    },
    "close": GO_BACK_MODAL,
    "blocks": [
        HEADER_MODAL,
        {
            "type": MODAL_TYPE_ACTIONS,
            "elements": [
                {
                    "type": MODAL_INPUT_TYPE_BUTTON,
                    "action_id": MODAL_VALUE_PROJECT_SHARED,
                    "text": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "Shared"
                    },
                    "value": MODAL_VALUE_PROJECT_SHARED
                },
                {
                    "action_id": MODAL_VALUE_PROJECT_FAST,
                    "type": MODAL_INPUT_TYPE_BUTTON,
                    "text": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "Fast"
                    },
                    "style": "primary",
                    "value": MODAL_VALUE_PROJECT_FAST
                }
            ]
        },
        ALERT_NAME_MODAL,
        {
            "type": MODAL_TYPE_INPUT,
            "block_id": "fast_account_name",
            "element": {
                "type": MODAL_INPUT_TYPE_PLAIN_TEXT,
                "action_id": "fast_account_name",
                "placeholder": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Enter the Account ID"
                }
            },
            "label": {
                "type": MODAL_TYPE_PLAIN_TEXT,
                "text": "Enter the Account ID"
            }
        },
        BUDGET_LIMIT_MODAL,
        BUDGET_THRESHOLD_MODAL,
        REPORT_SCHEDULE_MODAL,
        CHANNEL_SELECT_MODAL,
        PRIVATE_CHANNEL_INFO_MODAL_SECTION,
        VIEW_NOW_MODAL
    ]
}

MODAL_BUILDER_DATA_SHARED = {
    "type": "modal",
    "private_metadata": MODAL_VALUE_PROJECT_SHARED,
    "callback_id": MODAL_VALUE_PROJECT_SHARED,
    "title": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": MODAL_HEADER
    },
    "blocks": [
        HEADER_MODAL,
        {
            "type": MODAL_TYPE_ACTIONS,
            "elements": [
                {
                    "type": MODAL_INPUT_TYPE_BUTTON,
                    "action_id": MODAL_VALUE_PROJECT_SHARED,
                    "text": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "Shared"
                    },
                    "style": "primary",
                    "value": MODAL_VALUE_PROJECT_SHARED
                },
                {
                    "action_id": MODAL_VALUE_PROJECT_FAST,
                    "type": MODAL_INPUT_TYPE_BUTTON,
                    "text": {
                        "type": MODAL_TYPE_PLAIN_TEXT,
                        "text": "Fast"
                    },
                    "value": MODAL_VALUE_PROJECT_FAST
                }
            ]
        },
        ALERT_NAME_MODAL,
        PROJECT_TAG_MODAL,
        BUDGET_LIMIT_MODAL,
        BUDGET_THRESHOLD_MODAL,
        REPORT_SCHEDULE_MODAL,
        CHANNEL_SELECT_MODAL,
        PRIVATE_CHANNEL_INFO_MODAL_SECTION,
        VIEW_NOW_MODAL
    ],
    "submit": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Submit"
    },
    "close": GO_BACK_MODAL
}

MODAL_ENTRY_POINT = {
    "type": "modal",
    "title": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": MODAL_HEADER
    },
    "close": {
        "type": MODAL_TYPE_PLAIN_TEXT,
        "text": "Close"
    },
    "blocks": [
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_PLAIN_TEXT,
                "text": "This application helps to create Kmart cost notification for SHARED and FAST based accounts"
            }
        },
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_PLAIN_TEXT,
                "text": "It helps to schedule a notifier bot that gives you daily, weekly or monthly notifications on costing based on your own budget and threshold limits"
            }
        },
        {
            "type": MODAL_TYPE_DIVIDER
        },
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_PLAIN_TEXT,
                "text": "Please select an option to proceed: "
            }
        },
        {
            "type": MODAL_TYPE_DIVIDER
        },
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_MRK_DWN,
                "text": "Create a new notification"
            },
            "accessory": {
                "type": MODAL_INPUT_TYPE_BUTTON,
                "text": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Create"
                },
                "value": MODAL_VALUE_CREATE_ALERT,
                "action_id": MODAL_VALUE_CREATE_ALERT
            }
        },
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_MRK_DWN,
                "text": "Update an existing notification"
            },
            "accessory": {
                "type": MODAL_INPUT_TYPE_BUTTON,
                "text": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Update"
                },
                "value": MODAL_VALUE_UPDATE_ALERT,
                "action_id": MODAL_VALUE_UPDATE_ALERT
            }
        },
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_MRK_DWN,
                "text": "Delete an existing notification"
            },
            "accessory": {
                "type": MODAL_INPUT_TYPE_BUTTON,
                "text": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "Delete"
                },
                "value": MODAL_VALUE_DELETE_ALERT,
                "action_id": MODAL_VALUE_DELETE_ALERT
            }
        },
        {
            "type": MODAL_TYPE_SECTION,
            "text": {
                "type": MODAL_TYPE_MRK_DWN,
                "text": "View an existing notification"
            },
            "accessory": {
                "type": MODAL_INPUT_TYPE_BUTTON,
                "text": {
                    "type": MODAL_TYPE_PLAIN_TEXT,
                    "text": "View"
                },
                "value": MODAL_VALUE_INSTANT_ALERT,
                "action_id": MODAL_VALUE_INSTANT_ALERT
            }
        }
    ]
}
