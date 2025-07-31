import json
from datetime import datetime, date


def get_result(file_list, round_digits: int = 3, date_filter = None):
    if date_filter:
        date_filter = date.fromisoformat(date_filter)
    result = {}
    for file in file_list:
        with file:
            aggregated = aggregate_log_file(file, date_filter)
            for url, data in aggregated.items():
                if url in result:
                    result[url]['count'] += data['count']
                    result[url]['response_time'] += data['response_time']
                else:
                    result[url] = data
    for url in result:
        count = result[url]['count']
        total_time = result[url]['response_time']
        result[url]['response_time'] = round(total_time / count, round_digits)
    return result


def aggregate_log_file(file_obj, date_filter):
    result = {}
    
    for line in file_obj:
        try:
            row = json.loads(line)
            
            date_from_file = row.get('@timestamp')
            if date_from_file:
                line_timestamp = datetime.fromisoformat(date_from_file).date()
            if date_filter:
                if line_timestamp > date_filter:
                    break
                elif line_timestamp < date_filter:
                    continue
            url = row['url']
            response_time = row['response_time']
            if url in result:
                result[url]['count'] += 1
                result[url]['response_time'] += response_time
            else:
                result[url] = {'count': 1, 'response_time': response_time}
        except (json.JSONDecodeError, KeyError) as error:
            print(str(error))
            continue
    return result

