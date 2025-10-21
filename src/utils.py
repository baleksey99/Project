import json


def filter_transactions_by_currency(input_file):
    """Функция, которая принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях"""

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
            if not isinstance(transactions, list):
                raise TypeError("JSON-файл должен содержать список.")
            return transactions
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        print(f"Ошибка: {e}")
        return []
