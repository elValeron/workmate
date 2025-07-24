import pytest
from unittest.mock import MagicMock, mock_open, patch
from ..service import get_result, read_file

def test_read_file_with_mocked_data():
    """
    Тестирует read_file() с моком файла, проверяя обработку данных
    без реального доступа к файловой системе.
    """
    # 1. Подготовка тестовых данных
    test_data = [
        '{"url": "/api/users", "response_time": 0.12}\n',
        '{"url": "/api/products", "response_time": 0.23}\n',
        '{"url": "/api/users", "response_time": 0.15}\n'
    ]
    
    # 2. Создаем мок файла с тестовыми данными
    m = mock_open(read_data=''.join(test_data))
    
    # 3. Заменяем встроенную open на наш мок
    with patch('builtins.open', m):
        # 4. Вызываем тестируемую функцию
        result = read_file('test.log')
        
        # 5. Проверяем, что файл открывался правильно
        m.assert_called_once_with('test.log', 'r')
        
        # 6. Проверяем результаты обработки
        expected_result = {
            '/api/users': {
                'count': 2,
                'response_time': 0.27  # 0.12 + 0.15
            },
            '/api/products': {
                'count': 1,
                'response_time': 0.23
            }
        }
        
        assert result == expected_result

def test_read_file_with_empty_file():
    """Тест обработки пустого файла"""
    with patch('builtins.open', mock_open(read_data='')):
        result = read_file('empty.log')
        assert result == {}

def test_read_file_with_invalid_lines():
    """Тест обработки файла с некорректными строками"""
    test_data = [
        'invalid json\n',
        '{"url": "/api/valid", "response_time": 0.1}\n',
        '{"missing_fields": "value"}\n'
    ]
    
    with patch('builtins.open', mock_open(read_data=''.join(test_data))):
        result = read_file('invalid.log')
        assert result == {
            '/api/valid': {
                'count': 1,
                'response_time': 0.1
            }
        }



def test_get_result_single_file():
    """Тест обработки одного файла"""
    # Создаем мок файла с тестовыми данными
    mock_file = MagicMock()
    mock_file.name = "test1.log"
    
    # Мокаем read_file для возврата тестовых данных
    with patch('workmate.service.read_file', return_value={
        '/api/users': {'count': 2, 'response_time': 0.27},
        '/api/products': {'count': 1, 'response_time': 0.23}
    }):
        print(mock_file.name, 'ttttttttttttttttttttttttttttttt')
        result = get_result([mock_file])
        print(result, 'sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssd')
        assert result == {
            '/api/users': {'count': 2, 'response_time': round(0.27/2, 3)},
            '/api/products': {'count': 1, 'response_time': 0.23}
        }

def test_get_result_multiple_files():
    """Тест агрегации данных из нескольких файлов"""
    # Создаем моки файлов
    mock_file1 = MagicMock()
    mock_file1.name = "test1.log"
    mock_file2 = MagicMock()
    mock_file2.name = "test2.log"
    
    # Мокаем read_file для возврата разных данных для разных файлов
    read_file_side_effect = [
        {'/api/users': {'count': 2, 'response_time': 0.27}},
        {'/api/users': {'count': 1, 'response_time': 0.15},
         '/api/orders': {'count': 3, 'response_time': 0.45}}
    ]
    
    with patch('workmate.service.read_file', side_effect=read_file_side_effect):
        result = get_result([mock_file1, mock_file2])
        
        assert result == {
            '/api/users': {'count': 3, 'response_time': round(0.42/3, 3)},
            '/api/orders': {'count': 3, 'response_time': round(0.45/3, 3)}
        }

def test_get_result_empty_file_list():
    """Тест обработки пустого списка файлов"""
    result = get_result([])
    assert result == {}

def test_get_result_with_empty_file():
    """Тест обработки файла без данных"""
    mock_file = MagicMock()
    mock_file.name = "empty.log"
    
    with patch('workmate.service.read_file', return_value={}):
        result = get_result([mock_file])
        assert result == {}

def test_get_result_duplicate_urls():
    """Тест правильного суммирования данных при дублировании URL в разных файлах"""
    mock_file1 = MagicMock()
    mock_file1.name = "test1.log"
    mock_file2 = MagicMock()
    mock_file2.name = "test2.log"
    
    read_file_side_effect = [
        {'/api/users': {'count': 2, 'response_time': 0.27}},
        {'/api/users': {'count': 3, 'response_time': 0.35}}
    ]
    
    with patch('workmate.service.read_file', side_effect=read_file_side_effect):
        result = get_result([mock_file1, mock_file2])
        
        assert result['/api/users']['count'] == 5  # 2 + 3
        assert result['/api/users']['response_time'] == round(0.62/5, 3)  # 0.27 + 0.35