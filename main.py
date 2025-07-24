import argparse
from service import get_result

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', nargs='+', type=argparse.FileType('r'), help='Путь до файла')
parser.add_argument('--report', help='Название отчёта')
args = parser.parse_args()
if args is not None:
    get_result(args.file)
else:
    raise ValueError('args is empty')