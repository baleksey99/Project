import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        "Дата операции": [
            "2025-03-01", "2025-03-10", "2025-04-05",
            "2025-05-01", "2025-05-15"
        ],
        "Категория": [
            "Супермаркеты", "Супермаркеты", "Развлечения",
            "Супермаркеты", "Кафе"
        ],
        "Сумма операции": [100.0, 200.0, 500.0, 150.0, 300.0]
    })


@pytest.mark.parametrize(
    "category,start_date,expected_total",
    [
        ("Супермаркеты", "2025-03-01", 450.0),
        ("Развлечения", "2025-03-01", 500.0),
        ("Кафе", "2025-03-01", 300.0),
        ("Транспорт", "2025-03-01", 0.0),  # нет транзакций
    ]
)
def test_spending_by_category_total(sample_transactions, category, start_date, expected_total):
    result = spending_by_category(sample_transactions, category, start_date)
    assert result["total_spent"] == expected_total


def test_spending_by_category_monthly_breakdown(sample_transactions):
    result = spending_by_category(sample_transactions, "Супермаркеты", "2025-03-01")
    monthly = {item["month"]: item["total"] for item in result["monthly_breakdown"]}
    assert monthly["2025-03"] == 300.0
    assert monthly["2025-05"] == 150.0


def test_spending_by_category_empty_df():
    empty_df = pd.DataFrame(columns=["Дата операции", "Категория", "Сумма операции"])
    result = spending_by_category(empty_df, "Супермаркеты", "2025-03-01")
    assert result["total_spent"] == 0.0
    assert len(result["monthly_breakdown"]) == 0


def test_spending_by_category_invalid_date(sample_transactions):
    with pytest.raises(ValueError):
        spending_by_category(sample_transactions, "Супермаркеты", "некорректная_дата")
