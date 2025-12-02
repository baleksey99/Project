import unittest

import pandas as pd

from src.reports import spending_by_category


class TestReports(unittest.TestCase):

    def setUp(self):
        # Фикстура: тестовый DataFrame
        self.df = pd.DataFrame({
            "Дата операции": [
                "2025-01-10", "2025-01-15", "2025-02-20",
                "2025-03-05", "2025-04-10"
            ],
            "Категория": [
                "Супермаркеты", "Супермаркеты", "Развлечения",
                "Супермаркеты", "ЖКХ"
            ],
            "Сумма операции": [1000.0, 1500.0, 500.0, 2000.0, 3000.0]
        })

    def test_spending_by_category_normal(self):
        result = spending_by_category(self.df, "Супермаркеты", "2025-01-01")

        self.assertEqual(result["category"], "Супермаркеты")
        self.assertEqual(result["period"], "2025-01-01 – 2025-03-31")
        self.assertAlmostEqual(result["total_spent"], 4500.0)
        self.assertEqual(result["transactions_count"], 3)
        self.assertAlmostEqual(result["average_transaction"], 1500.0)
        self.assertEqual(len(result["monthly_breakdown"]), 2)
        self.assertEqual(result["monthly_breakdown"][0]["month"], "2025-01")
        self.assertAlmostEqual(result["monthly_breakdown"][0]["total"], 2500.0)
        self.assertEqual(result["monthly_breakdown"][1]["month"], "2025-03")
        self.assertAlmostEqual(result["monthly_breakdown"][1]["total"], 2000.0)

    def test_spending_by_category_no_data(self):
        result = spending_by_category(self.df, "Транспорт", "2025-01-01")
        self.assertEqual(result["total_spent"], 0.0)
        self.assertEqual(result["transactions_count"], 0)
        self.assertEqual(result["average_transaction"], 0.0)
        self.assertEqual(len(result["monthly_breakdown"]), 0)

    def test_spending_by_category_single_month(self):
        result = spending_by_category(self.df, "Развлечения", "2025-02-01")
        self.assertEqual(result["period"], "2025-02-01 – 2025-04-30")
        self.assertAlmostEqual(result["total_spent"], 500.0)
        self.assertEqual(result["transactions_count"], 1)
        self.assertEqual(len(result["monthly_breakdown"]), 1)
        self.assertEqual(result["monthly_breakdown"][0]["month"], "2025-02")

    def test_spending_by_category_invalid_date(self):
        with self.assertRaises(ValueError):
            spending_by_category(self.df, "Супермаркеты", "invalid-date")
