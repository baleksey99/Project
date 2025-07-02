import random

def filter_by_currency(transactions, currency):
    """Функция, которая принимает список транзакций и возвращает итератор, 
    который поочередно выдает транзакции,где валюта операции соответствует заданной """

    for transaction in transactions:
        if transaction['operationAmount']['currency']['code'] == currency:
            yield transaction


def transaction_descriptions(transactions, description):
    """Функция, которая принимает список словарей с транзакциями и
    возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(n):
    for _ in range(n):
        yield "{:04} {:04} {:04} {:04}".format(
            random.randint(0, 9999),
            random.randint(0, 9999),
            random.randint(0, 9999),
            random.randint(0, 9999)
        )



