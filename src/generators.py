import random


def filter_by_currency(transactions, currency):
    """Функция, которая принимает список транзакций и возвращает итератор,
    который поочередно выдает транзакции,где валюта операции соответствует заданной"""

    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency:
            yield transaction


def transaction_descriptions(transactions):
    """Функция, которая принимает список словарей с транзакциями и
    возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(n, start, stop):
    """Функция, которая может сгенерировать номера карт
     в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999"""
    for _ in range(n):
        yield "{:04} {:04} {:04} {:04}".format(
            random.randint(start, stop),
            random.randint(start, stop),
            random.randint(start, stop),
            random.randint(start, stop)
        )
