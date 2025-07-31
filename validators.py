import re

invalid_date_message = invalid_date_message = (
    'Неправильный формат даты.\n'
    'Введите дату в формате YYYY-MM-DD: Например 2025-25-06'
)

DATE_FORMAT_PATTERN = r'^\d{4}-([0][1-9]|1[0-2])-([0][1-9]|[1-2]\d|3[01])$'

def validate_date_format(date):
    if not date or not re.match(DATE_FORMAT_PATTERN, date):
        raise ValueError(invalid_date_message)

def check_args_is_not_empty(args):
    if not any(vars(args).values()):
        raise ValueError('Не задан ни один агумент!')
