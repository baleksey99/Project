
from unittest.mock import patch
import pandas as pd
import pytest
from src.utils import get_currency_rates, get_greeting, get_stock_prices, load_transactions


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Дата операции": ["2025-03-15", "2025-03-20"],
        "Номер карты": ["5814", "7512"],
        "Сумма операции": [1000.0, 2000.0],
        "Категория": ["Супермаркеты", "Развлечения"]
    })


@patch("pandas.read_excel")
def test_load_transactions_ok(mock_read, sample_df):
    mock_read.return_value = sample_df
    df = load_transactions("dummy.xlsx")
    assert len(df) == 2
    assert "Номер карты" in df.columns


@patch("pandas.read_excel")
def test_load_transactions_empty(mock_read):
    mock_read.return_value = pd.DataFrame()
    df = load_transactions("empty.xlsx")
    assert df.empty


@pytest.mark.parametrize(
    "hour,expected_greeting",
    [
        (6, "Доброе утро"), (11, "Доброе утро"),
        (12, "Добрый день"), (17, "Добрый день"),
        (18, "Добрый вечер"), (22, "Добрый вечер"),
        (23, "Доброй ночи"), (0, "Доброй ночи"),
        (5, "Доброй ночи")
    ]
)
def test_get_greeting(hour, expected_greeting):
    assert get_greeting(hour) == expected_greeting


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"USD": 73.21, "EUR": 87.08}}
    rates = get_currency_rates(["USD", "EUR"])
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert pytest.approx(rates[0]["rate"], 0.01) == 73.21


@patch("requests.get")
def test_get_stock_prices(mock_get):
    mock_get.return_value.json.return_value = {"Global Quote": {"05. price": "150.12"}}
    prices = get_stock_prices(["AAPL"])
    assert len(prices) == 1
    assert prices[0]["stock"] == "AAPL"
