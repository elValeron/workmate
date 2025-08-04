from io import StringIO
from unittest.mock import MagicMock, mock_open, patch

from ..service import aggregate_log_file, get_result


def test_aggregate_log_file_with_mocked_data():

    test_data = (
        '{'
        '"url": "/api/users", '
        '"response_time": 0.12, '
        '"@timestamp":"2025-06-22T13:59:47+00:00"'
        '}\n'
        '{'
        '"url": "/api/products", '
        '"response_time": 0.23, '
        '"@timestamp":"2025-06-22T13:59:47+00:00"'
        '}\n'
        '{'
        '"url": "/api/users", '
        '"response_time": 0.15'
        '}'
    )
    emulated_file = StringIO(test_data)
    emulated_file.name = 'test.log'
    result = aggregate_log_file(emulated_file, date_filter=None)
    expected_result = {
        '/api/users': {
            'count': 2,
            'response_time': 0.27
        },
        '/api/products': {
            'count': 1,
            'response_time': 0.23
        }
    }
    assert result == expected_result


def test_aggregate_log_file_with_empty_file():
    with patch('builtins.open', mock_open(read_data='')):
        result = aggregate_log_file('empty.log', date_filter=None)
        assert result == {}


def test_aggregate_log_file_with_invalid_lines():
    test_data = (
        'invalid json\n'
        '{'
        '"url": "/api/valid", '
        '"response_time": 0.1, '
        '"@timestamp":"2025-06-22T13:59:47+00:00"'
        '}\n'
        '{"missing_fields": "value"}\n'
        )

    emulated_file = StringIO(test_data)
    emulated_file.name = 'test.log'
    result = aggregate_log_file(emulated_file, None)
    assert result == {
        '/api/valid': {
            'count': 1,
            'response_time': 0.1
        }
    }


def test_get_result_single_file():
    """Тест обработки одного файла"""
    mock_file = MagicMock()
    mock_file.name = "test1.log"
    with patch('workmate.service.aggregate_log_file', return_value={
        '/api/users': {'count': 2, 'response_time': 0.27},
        '/api/products': {'count': 1, 'response_time': 0.23}
    }):

        result = get_result([mock_file])

        assert result == {
            '/api/users': {'count': 2, 'response_time': round(0.27/2, 3)},
            '/api/products': {'count': 1, 'response_time': 0.23}
        }


def test_get_result_multiple_files():
    """Тест агрегации данных из нескольких файлов"""

    mock_file1 = MagicMock()
    mock_file1.name = "test1.log"
    mock_file2 = MagicMock()
    mock_file2.name = "test2.log"
    read_file_side_effect = [
        {'/api/users': {'count': 2, 'response_time': 0.27}},
        {'/api/users': {'count': 1, 'response_time': 0.15},
         '/api/orders': {'count': 3, 'response_time': 0.45}}
    ]
    with patch(
        'workmate.service.aggregate_log_file',
        side_effect=read_file_side_effect
    ):
        result = get_result([mock_file1, mock_file2])
        assert result == {
            '/api/users': {'count': 3, 'response_time': round(0.42/3, 3)},
            '/api/orders': {'count': 3, 'response_time': round(0.45/3, 3)}
        }


def test_get_result_empty_file_list():
    result = get_result([])
    assert result == {}


def test_get_result_with_empty_file():
    mock_file = MagicMock()
    mock_file.name = "empty.log"
    with patch('workmate.service.aggregate_log_file', return_value={}):
        result = get_result([mock_file])
        assert result == {}


def test_get_result_duplicate_urls():
    mock_file1 = MagicMock()
    mock_file1.name = "test1.log"
    mock_file2 = MagicMock()
    mock_file2.name = "test2.log"
    read_file_side_effect = [
        {'/api/users': {'count': 2, 'response_time': 0.27}},
        {'/api/users': {'count': 3, 'response_time': 0.35}}
    ]
    with patch(
        'workmate.service.aggregate_log_file',
        side_effect=read_file_side_effect
    ):
        result = get_result([mock_file1, mock_file2])
        assert result['/api/users']['count'] == 5
        assert result['/api/users']['response_time'] == round(0.62/5, 3)
