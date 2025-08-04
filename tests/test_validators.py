import pytest
from argparse import Namespace
from ..validators import (
    check_args_is_not_empty,
    invalid_date_message,
    validate_date_format
)


@pytest.mark.parametrize(
    'valid_date',
    [
        '2025-01-01',
        '1999-12-31',
        '2024-02-29'
    ]
)
def test_validate_date_format_valid(valid_date):
    validate_date_format(valid_date)


@pytest.mark.parametrize(
    'invalid_date',
    [
        "2025-25-06",
        "2025-06-32",
        "25-06-2025",
        "2025/06/25",
        "2025-6-1",
        "",
    ]
)
def test_validate_date_invalid_format(invalid_date):
    with pytest.raises(ValueError, match=invalid_date_message):
        validate_date_format(invalid_date)


def test_check_args_is_not_empty():
    data = Namespace(file=['test.log'], report='average')
    check_args_is_not_empty(data)


@pytest.mark.parametrize(
    'arguments',
    [
        {},
        {'file': None, 'report': None},
        {'file': [], 'report': ''}
    ]
)
def test_check_args_is_empty(arguments):
    args = Namespace(**arguments)
    with pytest.raises(ValueError, match='Не задан ни один агумент!'):
        check_args_is_not_empty(args)
