from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date


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


