from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state
from src.widget import get_date
from src.processing import sort_by_date
from src.widget import mask_account_card
import pytest
from unittest.mock import patch
from src.external_api import convert_transaction_to_rub
from src.utils import filter_transactions_by_currency
import json

with open('Data/operations.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


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


@patch('requests.get')
def test_convert_transaction_to_rub(mock_get):
    # Настройка мока для requests.get
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'result': 100.0}

    # Подготовка тестовой транзакции
    transaction = {
        "operationAmount": {
            "currency": {"code": "USD"},
            "amount": "100"
        }
    }

    # Проверка результата
    result = convert_transaction_to_rub(transaction)
    assert result == 100.0
    mock_get.assert_called_once()


def test_filter_transactions_by_currency(tmp_path):
    # Создаем временный JSON файл
    data = [{
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "8221.37",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    }]
    file_path = tmp_path / "transactions.json"
    with open(file_path, 'w') as f:
        json.dump(data, f)

    # Запускаем тест
    result = filter_transactions_by_currency(file_path)
    assert result == data
