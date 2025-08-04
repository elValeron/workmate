import argparse
from prettytable import PrettyTable
from service import get_result
from validators import check_args_is_not_empty, validate_date_format

def main(parser: argparse.ArgumentParser, table: PrettyTable):
    parser.add_argument(
        '-d', '--date',
        help='Отчет по конкретной дате. Формат YYYY-mm-dd'
    )
    parser.add_argument(
        '-f', '--file',
        nargs='+',
        type=argparse.FileType('r'),
        help='Путь до файлов'
    )
    parser.add_argument(
        '-r', '--report',
        nargs='+',
        help='Название отчёта',
        default='average'
    )
    args = parser.parse_args()
    table.title = '_'.join([arg for arg in args.report])
    table.field_names = ['URL', 'Count', 'AVG_response_time']
    try:
        check_args_is_not_empty(args)
        if args.date:
            validate_date_format(args.date)
            table.title += ' ' + args.date
        result = get_result(args.file, date_filter=args.date)
        for url, data in result.items():
            table.add_row([url, data['count'], data['response_time']])
        return table

    except ValueError as error:
        print(str(error))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    table = PrettyTable()
    print(main(parser, table))