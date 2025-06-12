from typing import List, Dict
from datetime import datetime


def filter_by_state(list_of_dict: List[Dict[str, str]], state='EXECUTED') -> List[Dict[str, str]]:
    """Функция возвращащая список словарей, содержащий только те
     словари, у которых ключ state соответствует указанному значению"""
    filtered_list = []
    for dict in list_of_dict:
        for key, value in dict.items():
            if dict.get('state') == state:
                filtered_list.append(dict)
            else:
                continue
    return filtered_list


result = filter_by_state(list_of_dict=eval(input("Enter the list of dictionaries: ")))
print(result)


def sort_by_date(list_of_dict: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Сортирует список словарей по полю 'date' (дата)."""
    sorted_list_of_dict = sorted(list_of_dict, key=lambda x: datetime.fromisoformat(x['date']), reverse=reverse)
    return sorted_list_of_dict
