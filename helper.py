from configs.constants import *
import calendar
from datetime import timedelta
import re


def get_end_date_based_on_schedule(start_date, report_schedule):
    tomorrow_date = CURRENT_DATE + timedelta(1)
    if report_schedule == REPORT_TYPE_DAILY:
        next_date = CURRENT_DATE + datetime.timedelta(days=1)
        end_date = str(next_date.strftime(DATE_FORMAT_DEFAULT))
    elif report_schedule == REPORT_TYPE_WEEKLY:
        next_week_date = start_date + datetime.timedelta(days=-start_date.weekday(), weeks=1)
        end_date = str(next_week_date.strftime(DATE_FORMAT_DEFAULT))
        if end_date == CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT):
            end_date = tomorrow_date + datetime.timedelta(days=-tomorrow_date.weekday(), weeks=1)
            return end_date.strftime(DATE_FORMAT_DEFAULT)
    else:
        month_end_date = datetime.date(start_date.year, start_date.month,
                                       calendar.monthrange(start_date.year, start_date.month)[-1])
        end_date = str(month_end_date.strftime(DATE_FORMAT_DEFAULT))
        if end_date == CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT):
            end_date = datetime.date(tomorrow_date.year, tomorrow_date.month,
                                     calendar.monthrange(tomorrow_date.year, tomorrow_date.month)[-1]).strftime(
                DATE_FORMAT_DEFAULT)
    return end_date


def calculate_percentage(total_reached, absolute_total):
    try:
        percentage_reached = 100 * float(total_reached) / float(absolute_total)
        rounded_percentage = round(float(percentage_reached), DEFAULT_ROUND_VALUE)
        return str(rounded_percentage)
    except ZeroDivisionError:
        print('*** Division by Zero encountered ***')
        return '0'


def calculate_start_date(report_schedule, for_old=False):
    yesterday_date = CURRENT_DATE - timedelta(1)
    start_date = datetime.datetime.strftime(yesterday_date, DATE_FORMAT_DEFAULT)
    if report_schedule == REPORT_TYPE_MONTHLY:
        start_date = CURRENT_DATE.replace(day=1).strftime(DATE_FORMAT_DEFAULT)
        if for_old:
            start_date = (CURRENT_DATE.replace(day=1) - timedelta(1)).strftime(DATE_FORMAT_DEFAULT)
        if start_date == CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT) and not for_old:
            start_date = yesterday_date.replace(day=1).strftime(DATE_FORMAT_DEFAULT)
    elif report_schedule == REPORT_TYPE_WEEKLY:
        day = CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT)
        dt = datetime.datetime.strptime(day, DATE_FORMAT_DEFAULT)
        start = dt - timedelta(days=dt.weekday())
        start_date = start.strftime(DATE_FORMAT_DEFAULT)
        if start_date == CURRENT_DATE.strftime(DATE_FORMAT_DEFAULT):
            start = yesterday_date - timedelta(days=6)
            start_date = start.strftime(DATE_FORMAT_DEFAULT)
    return start_date


def get_start_date_for_prev_cost_calc(start_date_arg, report_schedule):
    start_date_obj = datetime.datetime.strptime(start_date_arg, DATE_FORMAT_DEFAULT)
    init_date = start_date_obj - timedelta(1)
    start_date = datetime.datetime.strftime(init_date, DATE_FORMAT_DEFAULT)
    if report_schedule == REPORT_TYPE_MONTHLY:
        start_date = init_date.replace(day=1).strftime(DATE_FORMAT_DEFAULT)
    elif report_schedule == REPORT_TYPE_WEEKLY:
        day = init_date.strftime(DATE_FORMAT_DEFAULT)
        dt = datetime.datetime.strptime(day, DATE_FORMAT_DEFAULT)
        start = dt - timedelta(days=dt.weekday())
        start_date = start.strftime(DATE_FORMAT_DEFAULT)
    return start_date


def date_arithmetic(date, count, type='subtraction'):
    if type == 'subtraction':
        return datetime.datetime.strptime(date, DATE_FORMAT_DEFAULT) - timedelta(count)


def round_float(float_num):
    return round(float(float_num), DEFAULT_ROUND_VALUE)


def calculate_trend_in_usage(current_usage_amount, past_usage_amount):
    try:
        trend_percentage = ((float(current_usage_amount) - float(past_usage_amount)) / float(past_usage_amount)) * 100
        is_trend_up = True if float(current_usage_amount) > float(past_usage_amount) else False
        return round(abs(trend_percentage)), is_trend_up
    except ZeroDivisionError:
        return 0, True


def format_currency_digits(amount):
    return "{:,}".format(float(amount))


def date_string_to_object(date_string, from_format=DATE_FORMAT_DEFAULT):
    return datetime.datetime.strptime(date_string, from_format)


def string_to_byte(string, format='utf-8'):
    return bytes(string, format)


def sort_string_with_numbers(text):
    try:
        value = float(text)
    except ValueError:
        value = text
    return value


def human_sorting_keys(text):
    return [sort_string_with_numbers(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text)]
