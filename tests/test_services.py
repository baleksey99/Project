import pytest

from src.services import investment_bank


@pytest.fixture
def sample_transactions():
    return [
        {"Дата операции": "2025-03-05", "Сумма операции": 1712.0},
        {"Дата операции": "2025-03-10", "Сумма операции": 847.5},
        {"Дата операции": "2025-04-01", "Сумма операции": 500.0},  # не в марте
    ]


@pytest.mark.parametrize(
    "month,limit,expected",
    [
        ("2025-03", 10, 10.5),   # 1712→1720 (8) + 847.5→850 (2.5) = 10.5
        ("2025-03", 50, 40.5),    # 1712→1750 (38) + 847.5→850 (2.5) = 40.5
        ("2025-04", 100, 0.0),
    ]
)
def test_investment_bank(sample_transactions, month, limit, expected):
    result = investment_bank(month, sample_transactions, limit)
    assert result == pytest.approx(expected, 0.01)
