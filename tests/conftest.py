import pytest
from src.widget import mask_account_card


@pytest.fixture
def numbers():
    return "1234 56** **** 5678"


@pytest.fixture
def mask_numbers():
    return "**7890"


@pytest.mark.parametrize(
    "info, expected_result",
    [
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        ("Счет 12345678901234567890", "Счет ******7890")
    ]
)
def test_mask_account_card(info, expected_result):
    assert mask_account_card(info) == expected_result


@pytest.fixture
def date():
    return "11.03.2024"


@pytest.fixture
def state():
    return "EXECUTED"


@pytest.fixture
def list_of_dicts():
    return [
        {'state': 'EXECUTED', 'value': 'some_value'},
        {'state': 'PENDING', 'value': 'another_value'}
    ]
