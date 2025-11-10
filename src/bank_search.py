import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    '''Функция, которая возвращает список словарей, у которых в описании есть данная строка.'''
    filtered_list = []
    for transaction in data:
        if re.search(search, transaction.get('description', ''), re.IGNORECASE):
            filtered_list.append(transaction)
    return filtered_list
