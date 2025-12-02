import json
import os
import unittest

from src.views import home_page


class TestHomePageWithoutMocks(unittest.TestCase):

    def setUp(self):
        """Подготавливаем пути к тестовым данным (в папке data/)."""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "../data")
        self.operations_file = os.path.join(self.test_data_dir, "operations.xlsx")
        self.settings_file = os.path.join(self.test_data_dir, "user_settings.json")

    def test_home_page_success(self):
        """Проверяем, что home_page возвращает корректный JSON."""
        result_str = home_page("2025-03-20 14:00:00")
        result = json.loads(result_str)

        # Проверяем наличие всех ожидаемых полей
        self.assertIn("greeting", result)
        self.assertIn("cards", result)
        self.assertIn("top_transactions", result)
        self.assertIn("currency_rates", result)
        self.assertIn("stock_prices", result)

        # Приветствие
        self.assertEqual(result["greeting"], "Добрый день")

        # Если есть транзакции — проверяем их
        if result["cards"]:
            self.assertEqual(len(result["cards"]), 1)
            self.assertEqual(result["cards"][0]["last_digits"], "5814")
            self.assertEqual(result["cards"][0]["total_spent"], 3000.0)
            self.assertEqual(result["cards"][0]["cashback"], 30.0)

        # Топ‑5 транзакций
        if result["top_transactions"]:
            self.assertEqual(len(result["top_transactions"]), 2)
            self.assertEqual(result["top_transactions"][0]["amount"], 2000.0)

        # Курсы валют (должны быть, если user_currencies не пустой)
        # В тестовом user_settings.json: ["USD"] → должен быть 1 курс
        self.assertEqual(len(result["currency_rates"]), 1)
        self.assertEqual(result["currency_rates"][0]["currency"], "USD")
        # rate может быть любым числом (API-ответ), но не 0.01 (это было ошибочно)
        self.assertGreater(result["currency_rates"][0]["rate"], 0.0)
        # Цены акций (должны быть, если user_stocks не пустой)
        self.assertEqual(len(result["stock_prices"]), 1)
        self.assertEqual(result["stock_prices"][0]["stock"], "AAPL")

    def test_home_page_invalid_date(self):
        """Проверяем обработку неверного формата даты."""
        result_str = home_page("некорректная дата")
        result = json.loads(result_str)
        self.assertEqual(result["error"], "Некорректный формат даты")

    def test_home_page_missing_operations_file(self):
        """Проверяем работу при отсутствии operations.xlsx."""
        temp_file = self.operations_file + ".tmp"

        try:
            # Имитируем отсутствие файла
            if os.path.exists(self.operations_file):
                os.rename(self.operations_file, temp_file)

            result_str = home_page("2025-03-20 14:00:00")
            result = json.loads(result_str)

            # Транзакции и карты должны быть пустыми
            self.assertEqual(result["cards"], [])
            self.assertEqual(result["top_transactions"], [])

            # Остальные поля должны присутствовать
            self.assertIn("greeting", result)
            self.assertIn("currency_rates", result)
            self.assertIn("stock_prices", result)

        finally:
            # Восстанавливаем файл
            if os.path.exists(temp_file):
                os.rename(temp_file, self.operations_file)
