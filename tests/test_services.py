import unittest

from src.services import investment_bank


class TestInvestmentBank(unittest.TestCase):

    def test_normal_case(self):
        transactions = [
            {"Дата операции": "2025-03-15", "Сумма операции": 1712.0},
            {"Дата операции": "2025-03-20", "Сумма операции": 847.5}
        ]
        result = investment_bank("2025-03", transactions, 50)
        self.assertAlmostEqual(result, 40.5)  # 38 + 12.5

    def test_no_transactions_in_month(self):
        transactions = [{"Дата операции": "2025-04-01", "Сумма операции": 1000.0}]
        result = investment_bank("2025-03", transactions, 10)
        self.assertEqual(result, 0.0)

    def test_exact_multiple(self):
        transactions = [{"Дата операции": "2025-03-10", "Сумма операции": 1000.0}]
        result = investment_bank("2025-03", transactions, 50)
        self.assertEqual(result, 0.0)

    def test_limit_10(self):
        transactions = [{"Дата операции": "2025-03-05", "Сумма операции": 123.4}]
        result = investment_bank("2025-03", transactions, 10)
        self.assertAlmostEqual(result, 6.6)  # округляем до 130 → 130 - 123.4 = 6.6

    def test_invalid_date_format(self):
        transactions = [{"Дата операции": "invalid", "Сумма операции": 100.0}]
        result = investment_bank("2025-03", transactions, 10)
        self.assertEqual(result, 0.0)

    def test_empty_transactions_list(self):
        """Проверяет работу с пустым списком транзакций."""
        result = investment_bank("2025-03", [], 50)
        self.assertEqual(result, 0.0)

    def test_negative_amount(self):
        """Проверяет обработку отрицательной суммы операции."""
        transactions = [
            {"Дата операции": "2025-03-10", "Сумма операции": -500.0},
            {"Дата операции": "2025-03-15", "Сумма операции": 1200.0}
        ]
        result = investment_bank("2025-03", transactions, 100)
        # Отрицательная сумма: округление до -500 → saved = 0 (т.к. -500 % 100 == 0)
        # 1200 → кратно 100 → saved = 0
        self.assertEqual(result, 0.0)

    def test_limit_100(self):
        """Проверяет округление с лимитом 100."""
        transactions = [
            {"Дата операции": "2025-03-01", "Сумма операции": 950.75},
            {"Дата операции": "2025-03-02", "Сумма операции": 1049.25}
        ]
        result = investment_bank("2025-03", transactions, 100)
        # 950.75 → округляем до 1000 → saved = 49.25
        # 1049.25 → округляем до 1100 → saved = 50.75
        self.assertAlmostEqual(result, 100.0)  # 49.25 + 50.75

    def test_multiple_currencies_or_formats(self):
        """Проверяет устойчивость к нестандартным типам данных (строка вместо числа)."""
        transactions = [
            {"Дата операции": "2025-03-10", "Сумма операции": "1500.50"},  # строка
            {"Дата операции": "2025-03-11", "Сумма операции": 2000.0}
        ]
        result = investment_bank("2025-03", transactions, 50)
        # "1500.50" → приведение к float → 1500.50 → saved = 49.50 (до 1550)
        # 2000.0 → кратно 50 → saved = 0
        self.assertAlmostEqual(result, 49.5)
