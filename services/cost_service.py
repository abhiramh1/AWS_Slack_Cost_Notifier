from services.client_service import init_aws_client, init_aws_client_cost_explorer
from configs.constants import *
from configs.configs import *
from datetime import timedelta
from helper import get_end_date_based_on_schedule, calculate_percentage, calculate_start_date, round_float, \
    calculate_trend_in_usage, get_start_date_for_prev_cost_calc, date_string_to_object, date_arithmetic
import dateutil
import botocore.errorfactory


def get_cost_explorer_result(linked_account, start_date, end_date, request_arg, env, is_previous=False):
    print('get_cost_explorer_result')
    linked_account_filtered = filter_linked_accounts(linked_account, env)
    print('linked_account_filtered: ')
    print(linked_account_filtered)
    # return INIT_AMOUNT, INIT_AMOUNT
    if len(linked_account_filtered) == 0:
        return INIT_AMOUNT, INIT_AMOUNT
    budget_limit = request_arg['budget_limit']
    report_schedule = request_arg['report_schedule']
    client = init_aws_client('ce')
    request_data = {
        'start_date': start_date,
        'end_date': end_date,
        'project_tag': request_arg['project_tag'],
        'linked_accounts': linked_account_filtered
    }
    query = build_ce_request_data(**request_data)
    result = client.get_cost_and_usage(**query)
    buffer, total_cost, threshold_reached = format_cost_explorer_result(result, budget_limit, report_schedule, is_previous)
    return total_cost, threshold_reached


def build_ce_request_data(**request_data):
    return {
        "TimePeriod": {
            "Start": request_data['start_date'],
            "End": request_data['end_date'],
        },
        "Granularity": "MONTHLY",
        "Filter": {
            "And": [
                {
                    "Dimensions": {
                        "Key": "LINKED_ACCOUNT",
                        "Values": request_data['linked_accounts']
                    }
                },
                {
                    "Tags": {
                        "Key": "Project",
                        "Values": [
                            request_data['project_tag']
                        ],
                        "MatchOptions": [
                            "EQUALS"
                        ]
                    }
                }
            ]
        },
        "Metrics": ["UnblendedCost"],
        "GroupBy": [
            {
                "Type": "DIMENSION",
                "Key": "SERVICE",
            },
        ],
    }


def get_cost_forecasting_result(total_cost, report_schedule):
    try:
        total_forecasted_amount = None
        start_date = CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT)
        end_date = get_end_date_based_on_schedule(CURRENT_DATE, report_schedule)
        formatted_end_date = (datetime.datetime.strptime(end_date, DATE_FORMAT_DEFAULT) + timedelta(1)).strftime(DATE_FORMAT_DEFAULT)
        client = init_aws_client('ce')
        request_data = {
            'start_date': start_date,
            'end_date': formatted_end_date
        }
        query = build_forecast_request_data(**request_data)
        result = client.get_cost_forecast(**query)
        if result['Total']['Amount']:
            amount = float(round(float(result['Total']['Amount']), DEFAULT_ROUND_VALUE))
            if amount != INIT_AMOUNT:
                total_forecasted_amount = round(total_cost + amount, DEFAULT_ROUND_VALUE)
        return str(total_forecasted_amount)
    except botocore.errorfactory.ClientError as e:
        print(str(e))
        return '0'


def build_forecast_request_data(**request_data):
    return {
        "TimePeriod": {
            "Start": request_data['start_date'],
            "End": request_data['end_date'],
        },
        "Granularity": "DAILY",
        "Filter": {
            "Tags": {
                "Key": "Project",
                "Values": [
                    "location"
                ],
                "MatchOptions": [
                    # "ABSENT"
                    "EQUALS"
                ]
            }
        },
        "Metric": "UNBLENDED_COST"
    }


def format_cost_explorer_result(result, budget_limit, report_schedule, is_previous):
    print('format_cost_explorer_result')
    time_range = ''
    total_cost_unformatted = INIT_AMOUNT
    threshold_reached = INIT_AMOUNT
    for result in result['ResultsByTime']:
        time_range = 'Cost from ' + result['TimePeriod']['Start'] + ' to ' + result['TimePeriod']['End'] + ' is \n'
        if report_schedule == REPORT_TYPE_DAILY:
            time_range = 'Daily cost is calculated as \n'
        if is_previous:
            time_range = 'Past ' + REPORT_SCHEDULE[report_schedule] + ' usage details: \n'
        for groups in result['Groups']:
            amount = float(round(float(groups['Metrics']['UnblendedCost']['Amount']), DEFAULT_ROUND_VALUE))
            if amount != INIT_AMOUNT:
                total_cost_unformatted += amount
        total_cost_reached = str(round(total_cost_unformatted, DEFAULT_ROUND_VALUE))
        threshold_reached = calculate_percentage(total_cost_reached, budget_limit)
    return time_range, total_cost_unformatted, threshold_reached


def calculate_trend_in_cost_usage(linked_accounts, request_arg, start_date, total_cost, env):
    try:
        report_schedule = request_arg['report_schedule']
        start_trend_date = modify_date_to_calculate_percentage_increase(start_date, report_schedule)
        end_trend_date = modify_date_to_calculate_percentage_increase(CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT), report_schedule)
        total_trend_cost, total_trend_threshold = get_cost_explorer_result(linked_accounts, start_trend_date, end_trend_date, request_arg, env=env)
        trend_percentage = ((float(total_cost) - float(total_trend_cost)) / float(total_trend_cost)) * 100
        is_trend_up = True if float(total_cost) > float(total_trend_cost) else False
        return round(abs(trend_percentage)), is_trend_up
    except ZeroDivisionError:
        return 0, True


def calculate_trend_in_forcasted_usage(forecast_amount, total_past_usage):
    try:
        trend_percentage = ((float(forecast_amount) - float(total_past_usage)) / float(total_past_usage)) * 100
        is_trend_up = True if float(forecast_amount) > float(total_past_usage) else False
        return round(abs(trend_percentage)), is_trend_up
    except ZeroDivisionError:
        return 0, True


def modify_date_to_calculate_percentage_increase(date, report_schedule):
    if report_schedule == REPORT_TYPE_MONTHLY:
        a_month = dateutil.relativedelta.relativedelta(months=1)
        date_minus_month = date_string_to_object(date_string=date) - a_month
        return date_minus_month.strftime(DATE_FORMAT_DEFAULT)
    elif report_schedule == REPORT_TYPE_WEEKLY:
        a_week = dateutil.relativedelta.relativedelta(weeks=1)
        date_minus_week = date_string_to_object(date_string=date) - a_week
        return date_minus_week.strftime(DATE_FORMAT_DEFAULT)
    else:
        a_day = dateutil.relativedelta.relativedelta(days=1)
        date_minus_day = date_string_to_object(date_string=date) - a_day
        return date_minus_day.strftime(DATE_FORMAT_DEFAULT)


def build_aws_service_usage_data(data_builder, service_details, service_provider, request_data):
    total_service_usage = INIT_AMOUNT
    total_past_service_usage = INIT_AMOUNT
    report_schedule = request_data['report_schedule']
    start_date = calculate_start_date(report_schedule)
    start_date_prev_cost_calc = get_start_date_for_prev_cost_calc(start_date, report_schedule)
    data_builder['services'][service_provider] = {}
    linked_accounts = generate_linked_account(start_date, CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT))
    for key, value in service_details['data'].items():
        data_builder['services'][service_provider][key] = {}
        data_builder['services'][service_provider][key]['label'] = value['label']
        data_builder['services'][service_provider][key]['emoji'] = value['emoji']
        data_builder['services'][service_provider][key]['total_cost_old'], data_builder['services'][service_provider][key]['threshold_reached_old'] = get_cost_explorer_result(linked_accounts, start_date_prev_cost_calc, start_date, request_data, env=value, is_previous=True)

        data_builder['services'][service_provider][key]['total_cost'], data_builder['services'][service_provider][key]['threshold_reached'] = get_cost_explorer_result(linked_accounts, start_date, CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT), request_data, env=value)

        # data_builder['services'][service_provider][key]['forecast_amount'] = get_cost_forecasting_result(data_builder['services'][service_provider][key]['total_cost'], report_schedule)

        data_builder['services'][service_provider][key]['trend_in_cost_usage'], \
        data_builder['services'][service_provider][key]['is_trend_up'] = calculate_trend_in_cost_usage(linked_accounts, request_data, start_date, data_builder['services'][service_provider][key]['total_cost'], env=value)

        data_builder['services'][service_provider][key]['aws_account_id'] = get_aws_account_id()

        data_builder['services'][service_provider][key]['total_cost_rounded'] = round_float(data_builder['services'][service_provider][key]['total_cost'])
        data_builder['services'][service_provider][key]['total_cost_old_rounded'] = round_float(data_builder['services'][service_provider][key]['total_cost_old'])

        data_builder['services'][service_provider][key]['trend_usage_percentage'], \
        data_builder['services'][service_provider][key]['is_trend_up'] = calculate_trend_in_usage(data_builder['services'][service_provider][key]['total_cost'],data_builder['services'][service_provider][key]['total_cost_old'])

        total_service_usage = total_service_usage + data_builder['services'][service_provider][key]['total_cost_rounded']
        total_past_service_usage = total_past_service_usage + data_builder['services'][service_provider][key]['total_cost_old_rounded']
    return {
        "total_service_usage": total_service_usage,
        "total_past_service_usage": total_past_service_usage
    }


def get_aws_account_id():
    sts = init_aws_client('sts')
    return sts.get_caller_identity()["Account"] if "Account" in sts.get_caller_identity() else None


def get_cost_tags(key='Project', search_string=''):
    raw_start_date = date_arithmetic(CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT), 365)
    start_date = raw_start_date.strftime(DATE_FORMAT_DEFAULT)
    end_date = CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT)
    client = init_aws_client('ce')
    response = client.get_tags(
        SearchString=search_string,
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        TagKey=key
    )
    return response


def generate_linked_account(start_date, end_date):
    linked_accounts = []
    client = init_aws_client('ce')
    response = client.get_dimension_values(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Dimension='LINKED_ACCOUNT',
        Context='COST_AND_USAGE'
    )
    for value in response['DimensionValues']:
        details = {
            "account_id": value['Value'],
            "account_name": value['Attributes']['description']
        }
        linked_accounts.append(details)
    return linked_accounts


def filter_linked_accounts(linked_account_list, env):
    account_name = generate_account_name_list(linked_account_list, env)
    filtered_list = [d['account_id'] for d in linked_account_list if d['account_name'] in account_name]
    return filtered_list


def generate_account_name_list(linked_account, env):
    environment = env['env']
    account_regex = env['regex']
    account_filtered_list = []
    if environment in [SERVICE_AWS_KEY_DEV, SERVICE_AWS_KEY_NON_PROD]:
        for account_name in linked_account:
            if account_regex in account_name['account_name']:
                print(account_name['account_name'])
                account_filtered_list.append(account_name['account_name'])

    elif environment == SERVICE_AWS_KEY_PROD:
        for account_name in linked_account:
            if account_regex in account_name['account_name'] and 'Non' not in account_name['account_name']:
                print(account_name['account_name'])
                account_filtered_list.append(account_name['account_name'])

    elif environment == SERVICE_AWS_KEY_SHARED:
        for account_name in linked_account:
            if account_name['account_name'] not in ['Production', 'Development']:
                print(account_name['account_name'])
                account_filtered_list.append(account_name['account_name'])

    return account_filtered_list
