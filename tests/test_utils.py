import unittest
from unittest.mock import patch

import pandas as pd

from src.utils import get_currency_rates, get_greeting, get_stock_prices, load_transactions


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.test_df = pd.DataFrame({
            "Дата операции": ["2025-03-15", "2025-03-20"],  # Исправлено!
            "Номер карты": ["5814", "7512"],
            "Сумма операции": [1000.0, 2000.0],
            "Категория": ["Супермаркеты", "Развлечения"]
        })

    @patch("pandas.read_excel")
    def test_load_transactions_ok(self, mock_read):
        mock_read.return_value = self.test_df
        df = load_transactions("dummy.xlsx")
        self.assertEqual(len(df), 2)
        self.assertIn("Номер карты", df.columns)

    def test_get_greeting(self):  # Обратите внимание: get_greeting vs get_greeting
        self.assertEqual(get_greeting(6), "Доброе утро")
        self.assertEqual(get_greeting(13), "Добрый день")
        self.assertEqual(get_greeting(19), "Добрый вечер")
        self.assertEqual(get_greeting(0), "Доброй ночи")

    @patch("requests.get")
    def test_get_currency_rates(self, mock_get):
        mock_get.return_value.json.return_value = {
            "rates": {"USD": 73.21, "EUR": 87.08}
        }
        rates = get_currency_rates(["USD", "EUR"])
        self.assertEqual(rates[0]["currency"], "USD")
        self.assertEqual(rates[0]["rate"], 73.21)
        self.assertEqual(rates[1]["currency"], "EUR")
        self.assertEqual(rates[1]["rate"], 87.08)

    @patch("requests.get")
    def test_get_stock_prices(self, mock_get):
        mock_get.return_value.json.return_value = {
            "Global Quote": {"05. price": "150.12"}
        }
        prices = get_stock_prices(["AAPL"])
        self.assertEqual(prices[0]["stock"], "AAPL")
        self.assertEqual(prices[0]["price"], 150.12)
