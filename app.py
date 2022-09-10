from flask import Flask, json, request, make_response
from services.modal_service import *
from services.client_service import client_view_actions, send_data_to_client_formatted, init_aws_client, \
    client_conversation_name, init_aws_resource
from services.queue_service import init_queue
from services.cost_service import build_aws_service_usage_data
from services.storage_service import upload_user_details_file_to_s3, is_file_available_in_s3
from helper import calculate_percentage, calculate_start_date, get_end_date_based_on_schedule, round_float, \
    calculate_trend_in_usage
from configs.constants import *
from configs.configs import *
from services.auth_service import authenticate_request
import time

app = Flask(__name__)


@app.before_request
def before_request():
    try:
        print('App Index point')
        authenticate_request(request)
    except (AttributeError, ConnectionError, TypeError) as e:
        print('before_request: ' + str(e))
        return make_response({"text": 'You are not authorized to perform this action'})


# Features->Slash Commands->Request URL
@app.route('/modal', methods=['POST'])
def modal_index():
    try:
        print('Modal entry point: Modal popup comes up')
        trigger_id = request.form.get('trigger_id')
        client_view_actions(CLIENT_API_VIEW_OPEN, trigger_id, MODAL_ENTRY_POINT)
        return make_response()
    except Exception as e:
        print('modal_index: ' + str(e))
        return make_response({"text": "Internal server error. Please try again!!"})


# Features->Interactivity & Shortcuts->Request URL
@app.route('/action', methods=['POST'])
def action():
    try:
        request_data = request.form
        json_decoded_payload = json.loads(request_data['payload'])

        # Type = view_submission when a submit button is triggered
        if json_decoded_payload['type'] == 'view_submission':
            submission_state_details = json_decoded_payload['view']['state']['values']
            action_type = json_decoded_payload['view']['private_metadata']

            project_tag = None
            fast_account_name = None

            if action_type in [MODAL_VALUE_PROJECT_SHARED, MODAL_VALUE_UPDATE_PROJECT_SHARED]:
                project_tag = get_submission_state_value(submission_state_details, MODAL_VALUE_PROJECT_TAG, field_type='selected_option')
            if action_type == MODAL_VALUE_PROJECT_FAST:
                fast_account_name = get_submission_state_value(submission_state_details, MODAL_VALUE_FAST_ACCOUNT_NAME, field_type=MODAL_INPUT_TYPE_PLAIN_TEXT)

            budget_limit = get_submission_state_value(submission_state_details, MODAL_VALUE_BUDGET_LIMIT, field_type=MODAL_INPUT_TYPE_PLAIN_TEXT)
            budget_threshold = get_submission_state_value(submission_state_details, MODAL_VALUE_BUDGET_THRESHOLD, field_type=MODAL_INPUT_TYPE_PLAIN_TEXT)
            channel_id = get_submission_state_value(submission_state_details, MODAL_VALUE_CHANNEL_ID, field_type='selected_option')
            report_schedule = get_submission_state_value(submission_state_details, MODAL_VALUE_REPORT_SCHEDULE, field_type='selected_option')
            send_now = get_submission_state_value(submission_state_details, MODAL_VALUE_SEND_NOW, field_type=MODAL_INPUT_TYPE_CHECKBOX)
            alert_name = get_submission_state_value(submission_state_details, MODAL_VALUE_ALERT_NAME, field_type=MODAL_INPUT_TYPE_PLAIN_TEXT)

            request_payload = {
                'report_schedule': report_schedule,
                'budget_threshold': budget_threshold,
                'channel_id': channel_id,
                "budget_limit": budget_limit,
                "account_type": action_type,
                "send_now": send_now,
                "project_tag": project_tag,
                "fast_account_name": fast_account_name,
                "alert_name": alert_name,
                "user_details": json_decoded_payload['user']
            }

            if action_type == MODAL_VALUE_INSTANT_ALERT:
                alert_name_response = send_instant_alert(json_decoded_payload, request)
                completion_text = ':white_check_mark: Your request to view the notification *' + alert_name_response + '* has processed successfully.'
                time.sleep(1)
                return make_response(view_actions('update', build_generate_completion_modal(completion_text)))
            if action_type == MODAL_VALUE_DELETE_ALERT:
                alert_name_response = make_alert_inactive(json_decoded_payload)
                completion_text = ':white_check_mark: Your request to delete the notification *' + alert_name_response + '* has processed successfully.'
                return make_response(view_actions('update', build_generate_completion_modal(completion_text)))
            if action_type == MODAL_VALUE_UPDATE_ALERT:
                payload = build_update_modal(json_decoded_payload)
                return make_response(view_actions('update', payload))
            if action_type == 'update_project_shared':
                request_payload['report_id'] = json_decoded_payload['view']['callback_id']
                data = {
                    "request_payload": request_payload,
                    "is_instant_alert": False,
                    "is_update": True
                }
                init_queue(data, request)
                completion_text = ':white_check_mark: Your request to update the notification *' + alert_name + '* has processed successfully.'
                time.sleep(1)
                return make_response(view_actions('update', build_generate_completion_modal(completion_text)))

            if not budget_limit.isnumeric():
                return make_response(validation_error(MODAL_VALUE_BUDGET_LIMIT), HTTP_STATUS_CODE_200)
            if not budget_threshold.isnumeric():
                return make_response(validation_error(MODAL_VALUE_BUDGET_THRESHOLD), HTTP_STATUS_CODE_200)

            data = {
                "request_payload": request_payload,
                "is_instant_alert": False
            }
            init_queue(data, request)
            block = build_plain_message("The requested notification *" + alert_name + "* is created. Thank you for the subscription.")
            send_data_to_client_formatted(block, channel_id)
            completion_text = ':white_check_mark: Your request to create notification *' + alert_name + '* has processed successfully.'
            time.sleep(1)
            return make_response(view_actions('update', build_generate_completion_modal(completion_text)))

        # Type = block_actions when any interactive action is triggered
        elif json_decoded_payload['type'] == 'block_actions':
            block_action_details = json_decoded_payload['actions'][0]['value']
            if block_action_details in [MODAL_VALUE_CREATE_ALERT, MODAL_VALUE_PROJECT_SHARED, MODAL_VALUE_PROJECT_FAST]:
                payload = MODAL_BUILDER_DATA_SHARED
            # elif block_action_details == MODAL_VALUE_PROJECT_FAST:
            #     payload = MODAL_BUILDER_DATA_FAST
            elif block_action_details == MODAL_VALUE_INSTANT_ALERT:
                payload = build_modal_alert_listing(MODAL_VALUE_INSTANT_ALERT, "view")
            elif block_action_details == MODAL_VALUE_DELETE_ALERT:
                payload = build_modal_alert_listing(MODAL_VALUE_DELETE_ALERT, "delete")
            elif block_action_details == MODAL_VALUE_UPDATE_ALERT:
                payload = build_modal_alert_listing_for_update(MODAL_VALUE_UPDATE_ALERT, 'update', 'Proceed to Update')
            elif block_action_details == 'build_update_modal':
                init_queue(json_decoded_payload, request)
                return make_response()
            else:
                payload = MODAL_ENTRY_POINT
            trigger_id = json_decoded_payload['trigger_id']
            client_view_actions(CLIENT_API_VIEW_PUSH, trigger_id, payload)

        # unknown request
        else:
            return make_response({"message": "Unknown request type."}, HTTP_STATUS_CODE_401)
        return make_response()
    except Exception as e:
        print('action: ' + str(e))
        return make_response({"text": "Internal server error. Please try again!!"})


# Master function which calculates the aws billing details and send alert to client client(slack)
@app.route('/process-cost-details/<request_data>', methods=['POST'])
def dispatch(request_data, is_instant_alert=False, is_update=False, is_from_scheduler=False):
    if request_data == 'from_api_request':
        request_data = request.get_json()['request_payload']
    if not is_from_scheduler and request.get_json():
        is_instant_alert = request.get_json()['is_instant_alert'] if 'is_instant_alert' in request.get_json() else is_instant_alert
        is_update = request.get_json()['is_update'] if 'is_update' in request.get_json() else is_update
    print('inside dispatch function under queuing..')
    total_service_usage = INIT_AMOUNT
    total_past_service_usage = INIT_AMOUNT
    report_schedule = request_data['report_schedule']
    budget_limit = request_data['budget_limit']
    budget_threshold = request_data['budget_threshold']
    channel_id = request_data['channel_id']
    start_date = calculate_start_date(report_schedule)
    if request_data['send_now']:
        data_builder = {
            "services": {}
        }
        data_builder_list = []
        for service_details in ALL_SERVICES_DETAILS:
            if service_details['key'] == 'aws':
                aws_usage = build_aws_service_usage_data(data_builder, service_details, service_details['key'], request_data)
                total_service_usage = total_service_usage + aws_usage['total_service_usage']
                total_past_service_usage = total_past_service_usage + aws_usage['total_past_service_usage']
            if service_details['key'] == 'github':
                # TODO github cost details API comes here
                pass

        data_builder['total_service_usage'] = round_float(total_service_usage)
        data_builder['total_past_service_usage'] = round_float(total_past_service_usage)
        data_builder['total_budget'] = round_float(budget_limit)
        data_builder['trend_usage_percentage'], data_builder['is_trend_up'] = calculate_trend_in_usage(data_builder['total_service_usage'], data_builder['total_past_service_usage'])
        data_builder['trend_budget_utilised'] = calculate_percentage(data_builder['total_service_usage'], budget_limit)
        data_builder['is_threshold_breached'] = False if float(budget_threshold) > float(data_builder['trend_budget_utilised']) else True
        data_builder['budget_limit'] = budget_limit
        data_builder['start_date'] = start_date
        data_builder['end_date'] = CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT)
        data_builder['report_schedule'] = report_schedule
        data_builder['alert_name'] = request_data['alert_name']
        data_builder_list.append(data_builder)
        block_regular_alert = build_alert_block_updated(data_builder_list[0])

        if is_from_scheduler:
            is_alert_send = False
            if data_builder['is_threshold_breached'] or (request_data['next_scheduled_alert_date'] == CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT)):
                send_data_to_client_formatted(block_regular_alert, channel_id)
                is_alert_send = True
            return is_alert_send
        else:
            print('Instant alert details sending to slack..')
            send_data_to_client_formatted(block_regular_alert, channel_id)
            print('completed dispatch function under queuing successfully..')
    print("After Slack message send..")
    if not is_instant_alert and not is_update and not is_from_scheduler:
        upload_user_details_file_to_s3(request_data)
    if not is_instant_alert and is_update and not is_from_scheduler:
        update_alert_details(request_data)
    return make_response('Notification details fetched and send to client successfully.')


# Features->Select Menus->Options Load URL
@app.route('/load-external-menus', methods=['POST'])
def load_external_menus():
    try:
        request_data = request.form
        json_decoded_payload = json.loads(request_data['payload'])
        search_string = json_decoded_payload['value']
        external_menu_type = json_decoded_payload['action_id']
        if external_menu_type in [MODAL_VALUE_ALERT_LIST, MODAL_VALUE_DELETE_ALERT, MODAL_VALUE_UPDATE_ALERT]:
            external_menu_options = load_alert_list_for_dropdown(json_decoded_payload)
        elif external_menu_type == MODAL_VALUE_CHANNEL_ID:
            external_menu_options = load_channel_list_for_dropdown(json_decoded_payload)
        else:
            external_menu_options = load_project_tag_details(search_string)
        return {
            "options": external_menu_options
        }
    except Exception as e:
        print('load_external_menus: ' + str(e))
        return make_response({"text": "Internal server error. Please try again!!"})


def get_submission_state_value(payload, key, field_type, is_predefined=False):
    try:
        if field_type == MODAL_INPUT_TYPE_PLAIN_TEXT:
            return payload[key][key]['value']
        elif field_type == 'selected_option' and not is_predefined:
            return payload[key][key]['selected_option']['value']
        elif field_type == 'selected_option' and is_predefined:
            return payload[key][key]['selected_conversation']
        elif field_type == 'checkboxes':
            return STATUS_ACTIVE if payload[key][key]['selected_options'] else STATUS_INACTIVE
    except KeyError:
        return None


'''Cron JOB API Start'''


@app.route('/init/scheduler', methods=['GET'])
def init_scheduler(event, context):
    client = init_aws_client('s3')
    resource = init_aws_resource('s3')
    user_alert_details = resource.Bucket(S3_BUCKET_NAME)
    summaries = user_alert_details.objects.all()
    for objects in summaries:
        process_file_in_scheduler(objects.key, client)
    return 'success'


def process_file_in_scheduler(file_name, client):
    user_scheduler_details = client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
    user_scheduler_details = user_scheduler_details['Body'].read()
    converted_payload = json.loads(user_scheduler_details.decode("utf-8"))

    # process ce apis
    for request_data in converted_payload:
        request_data['send_now'] = STATUS_ACTIVE
        if request_data['active']:
            alert_send = dispatch(request_data, is_instant_alert=False, is_update=False, is_from_scheduler=True)
            if alert_send and request_data['next_scheduled_alert_date'] == CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT):
                update_alert_details(request_data)


def is_given_threshold_crossed(threshold_input, current_threshold_reached):
    return True if float(current_threshold_reached) >= float(threshold_input) else False


'''Cron JOB API End'''


def get_existing_alert_details(request_payload):
    submission_state_details = request_payload['view']['state']['values']
    report_id = get_submission_state_value(submission_state_details, 'alert_list', field_type='selected_option')
    user_id = request_payload['user']['id']
    file_name = user_id + '.json'
    alert_details = is_file_available_in_s3(file_name)
    alert_data = next(item for item in alert_details if item["report_id"] == report_id)
    return alert_data, alert_details, file_name


def send_instant_alert(request_payload, request):
    request_data, total_details, file_name = get_existing_alert_details(request_payload)
    request_data['send_now'] = STATUS_ACTIVE
    data = {
        "request_payload": request_data,
        "is_instant_alert": True
    }
    init_queue(data, request)
    return request_data['alert_name']


def make_alert_inactive(request_payload):
    request_data, total_details, file_name = get_existing_alert_details(request_payload)
    request_data['active'] = False
    upload_user_details_file_to_s3(total_details, is_update=True, file_name_to_update=file_name)
    block = build_plain_message("The requested notification *" + request_data['alert_name'] + "* is deleted.")
    send_data_to_client_formatted(block, request_data['channel_id'])
    return request_data['alert_name']


def update_alert_details(request_payload):
    file_name = request_payload['user_details']['id'] + '.json'
    alert_details = is_file_available_in_s3(file_name)
    item_to_update = next(item for item in alert_details if item["report_id"] == request_payload['report_id'])
    if request_payload['channel_id'] != item_to_update['channel_id']:
        old_channel_id = item_to_update['channel_id']
        block = build_plain_message("The requested notification *" + request_payload['alert_name'] + "* is now unsubscribed from the channel.")
        send_data_to_client_formatted(block, old_channel_id)
    item_to_update['alert_name'] = request_payload['alert_name']
    item_to_update['budget_limit'] = request_payload['budget_limit']
    item_to_update['budget_threshold'] = request_payload['budget_threshold']
    item_to_update['channel_id'] = request_payload['channel_id']
    item_to_update['project_tag'] = request_payload['project_tag']
    item_to_update['report_schedule'] = request_payload['report_schedule']
    item_to_update['next_scheduled_alert_date'] = get_end_date_based_on_schedule(CURRENT_DATE, request_payload['report_schedule'])
    upload_user_details_file_to_s3(alert_details, is_update=True, file_name_to_update=file_name)
    block = build_plain_message("The requested notification *" + request_payload['alert_name'] + "* is updated.")
    send_data_to_client_formatted(block, request_payload['channel_id'])


def build_update_modal(request_payload):
    request_data, total_details, file_name = get_existing_alert_details(request_payload)
    channel_details = client_conversation_name(request_data['channel_id'])
    request_data['channel_name'] = request_data['user_details']['name']
    if channel_details:
        request_data['channel_name'] = channel_details['channel']['name']
    return build_update_modal_shared(request_data)


if __name__ == '__main__':
    app.run(port=SYSTEM_PORT, debug=True)
