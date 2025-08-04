
Анализатор логов workmate
## Описание
    - Анализатор кода - скрипт для анализа логов, таблицу с URL, количеством переходов по url и средним временем ответа.

## Стэк: 
    - python 3.12
    - argparse - парсинг аргументов командной строки
    - pytest - тесты
    - unittest - mock'и для имитации работы с файлами
    - prettytable - вывод результата в консоль

## Инструкция

### Настройка:
    1. Клонировать репозиторий командой:
        ```
        - git clone https://github.com/elValeron/workmate.git
        ```
    2. Создать и активировать виртуальное окружение:
        ```
        - python3 -m venv venv && source venv/bin/activate
        ```
### Использование:

    Скрипт запускается из корневой директории с указанием параметров:
    ```
        python main.py -f <filename>.log <filename2>.log -d <date> --report <report_name>
    ```
    Обязательные аргументы:

        '-f'|'--file' - список файлов указываемый через пробел
    
    Не обязательные аргументы: 

        '-d'|'--date' - дата в формате YYYY-mm-dd для парсинга данных за указанную дату

        '-r'|'--report' - название отчёта, по умолчанию average

### Примеры использования:
    Вывод со всеми параметрами:
    <img width="1085" height="212" alt="Image" src="https://github.com/user-attachments/assets/a7d82e73-6cdc-4640-a088-c52c72014e1b" />
    


Автор [elValeron](https://github.com/elValeron/)
