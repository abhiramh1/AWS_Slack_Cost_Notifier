from services.client_service import init_aws_client
from botocore.exceptions import ClientError
from helper import get_end_date_based_on_schedule, human_sorting_keys
from configs.constants import NO_SUCH_KEY_ERROR, CURRENT_DATE
from configs.configs import S3_BUCKET_NAME
import json


def upload_user_details_file_to_s3(file_content, is_update=False, file_name_to_update=None):
    print('S3 upload starting...')
    if file_name_to_update:
        file_name = file_name_to_update
    else:
        file_name = file_content['user_details']['id'] + '.json'
    # check if user file already exists
    if is_update:
        file_content_updated = file_content
    else:
        existing_user_schedule_details = is_file_available_in_s3(file_name)
        if not existing_user_schedule_details:
            file_content_updated = build_insert_details(file_content)
        else:
            file_content_updated = build_updated_details(file_content, existing_user_schedule_details)
    object_name = '/tmp/' + file_name
    file_open = open(object_name, 'w')
    file_open.write(json.dumps(file_content_updated))
    file_open.close()
    s3_client = init_aws_client('s3')
    s3_client.upload_file(object_name, S3_BUCKET_NAME, file_name)
    print('after s3 insert')


def is_file_available_in_s3(file_name):
    try:
        s3_client = init_aws_client('s3')
        user_scheduler_details = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_name)
        user_scheduler_details = user_scheduler_details['Body'].read()
        return json.loads(user_scheduler_details.decode("utf-8"))
    except ClientError as ex:
        if ex.response['Error']['Code'] == NO_SUCH_KEY_ERROR:
            return False


def build_insert_details(file_content):
    user_details_array = []
    # being the first user data start with 1
    file_content['report_id'] = file_content['user_details']['id'] + '_1'
    file_content['is_alert_send'] = False
    file_content['active'] = True
    file_content['next_scheduled_alert_date'] = get_end_date_based_on_schedule(CURRENT_DATE, file_content['report_schedule'])
    user_details_array.append(file_content)
    return user_details_array


def build_updated_details(file_content, existing_content):
    report_id_list = [report_id['report_id'] for report_id in existing_content]
    report_id_list.sort(key=human_sorting_keys)
    current_report_id = report_id_list[-1]
    latest_report_id = str(int(current_report_id.split('_')[-1]) + 1)
    file_content['report_id'] = file_content['user_details']['id'] + '_' + latest_report_id
    file_content['is_alert_send'] = False
    file_content['active'] = True
    file_content['next_scheduled_alert_date'] = get_end_date_based_on_schedule(CURRENT_DATE, file_content['report_schedule'])
    existing_content.append(file_content)
    return existing_content
