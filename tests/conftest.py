import pytest


@pytest.fixture
def numbers():
    return "1234 56** **** 5678"


@pytest.fixture
def mask_numbers():
    return "**7890"


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
