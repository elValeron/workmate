from prettytable import PrettyTable


table = PrettyTable()
table.title = 'My Table'
table.field_names = (
    'URL',
    'Количество',
    'Среднее время отклика'
)

print(table)