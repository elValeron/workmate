from pprint import pprint
import json

def get_result(file_list: list) -> dict[str, int|str]:
    result = {}
    for file in file_list:
        for key, value in read_file(file.name).items():
            if key in result:
                result[key]['count'] += value['count']
                result[key]['response_time'] += value['response_time']
            else:
                result[key] = value
    for key, value in result.items():
        result[key]['response_time'] = round(result[key]['response_time']/result[key]['count'], 3)
    print(result)
    return result

def read_file(filename: str) -> dict[str, int|str]:
    result = {}
    with open(filename, 'r') as file:
        
        for line in file:
            try:
                row = json.loads(line)
                url = row['url']
                response_time = row['response_time']

                if url in result:
                    result[url]['count'] += 1
                    result[url]['response_time'] += response_time
                else:
                    result[url] = {'count': 1, 'response_time': response_time}
            except json.JSONDecodeError as error:
                print(str(error))
                continue
            except KeyError as error:
                print(str(error))
                continue
    return result 
        

