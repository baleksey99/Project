import json
import logging

logger = logging.getLogger('utils')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/utils.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def filter_transactions_by_currency(input_file):
    """Функция, которая принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях"""

    try:
        logger.info("Запрашиваем информацию из файла")
        with open(input_file, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
            if not isinstance(transactions, list):
                logger.warning("В файле отсутствует список")
                raise TypeError("JSON-файл должен содержать список.")
            return transactions
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as ex:
        print(f"Ошибка: {ex}")
        logger.error(f"Произошла ошибка: {ex}")
        return []
