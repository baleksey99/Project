import re

import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


def test_get_mask_card_number(numbers):
    assert get_mask_card_number('1234567812345678') == numbers
    assert get_mask_card_number('1234 5678 1234 5678') == numbers
    assert get_mask_card_number('12345678123456') == ""


def test_get_mask_account(mask_numbers):
    assert get_mask_account('12345678901234567890') == mask_numbers
    assert get_mask_account('1234567 8901234567890') == mask_numbers
    assert get_mask_account('5678901234567890') == ""


def test_get_date(date):
    assert get_date('2024-03-11') == date
    assert get_date('') == ''


def test_filter_by_state(list_of_dicts, state):
    assert filter_by_state(list_of_dicts, state) == [{'state': 'EXECUTED', 'value': 'some_value'}]


@pytest.mark.parametrize(
    "info, expected_result",
    [
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        ("Счет 12345678901234567890", "Счет **7890")
    ]
)
def test_mask_account_card(info, expected_result):
    assert mask_account_card(info) == expected_result


@pytest.mark.parametrize(
    "input_list, reverse, expected_result",
    [
        # Тесты для reverse=True (по убыванию)
        (
            [{'date': '2022-01-01'}, {'date': '2021-01-01'}],
            True,
            [{'date': '2022-01-01'}, {'date': '2021-01-01'}]
        ),
        (
            [{'date': '2021-01-01'}, {'date': '2022-01-01'}],
            True,
            [{'date': '2022-01-01'}, {'date': '2021-01-01'}]
        ),
        # Тесты для reverse=False (по возрастанию)
        (
            [{'date': '2022-01-01'}, {'date': '2021-01-01'}],
            False,
            [{'date': '2021-01-01'}, {'date': '2022-01-01'}]
        ),
    ]
)
def test_sort_by_date(input_list, reverse, expected_result):
    assert sort_by_date(input_list, reverse=reverse) == expected_result


@pytest.mark.parametrize('transactions, currency, expected', [
    ([{
        "id": "939719570",
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }], "USD", [
        {
            "id": "939719570",
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        }
    ]),
    ([{
        "id": "939719570",
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "",
                "code": ""
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }], "USD", []),
    ([], "USD", [])
])
def test_filter_by_currency(transactions, currency, expected):
    assert list(filter_by_currency(transactions, currency)) == expected


@pytest.mark.parametrize('transactions, expected', [
    ([{
        "id": "939719570",
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }], ["Перевод организации"]),
    ([{
        "id": "939719570",
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    }], ["Перевод организации"]),
    ([], [])
])
def test_transaction_descriptions(transactions, expected):
    assert list(transaction_descriptions(transactions)) == expected


@pytest.mark.parametrize("n, start, stop", [
    (1, 1000, 9999),
    (5, 2000, 8000),
    (10, 3000, 7000)
])
def test_card_number_generator(n, start, stop):
    card_gen = card_number_generator(n, start, stop)
    count = 0
    for card in card_gen:
        # Проверка формата
        assert re.match(r"\d{4} \d{4} \d{4} \d{4}", card)
        count += 1
    # Убедись, что генератор выдал ровно n номеров
    assert count == n
