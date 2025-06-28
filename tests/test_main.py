from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state
from src.widget import get_date
from src.processing import sort_by_date
from src.widget import mask_account_card
import pytest


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
