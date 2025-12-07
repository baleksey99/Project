import json
from unittest.mock import patch
import pandas as pd
from src.views import home_page


@patch("src.utils.load_transactions")
@patch("src.utils.get_currency_rates")
@patch("src.utils.get_stock_prices")
def test_home_page_success(mock_load, mock_rates, mock_stocks):

    mock_load.return_value = pd.DataFrame({
        "Дата операции": ["2025-03-05", "2025-03-10", "2025-04-01"],
        "Номер карты": ["5814", "5814", "7512"],
        "Сумма операции": [1000.0, 500.0, 2000.0],
        "Категория": ["Супермаркеты", "Кафе", "Развлечения"],
        "Описание": ["Покупка продуктов", "Обед", "Кино"]
    })

    mock_rates.return_value = [
        {"currency": "USD", "rate": 73.5},
        {"currency": "EUR", "rate": 80.2}
    ]

    # Мок для get_stock_prices
    mock_stocks.return_value = [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "GOOGL", "price": 135.88}
    ]

    # 2. Вызываем тестируемую функцию
    result_str = home_page("2025-03-15 14:00:00")
    result = json.loads(result_str)

    # 3. Проверки
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result
    assert result["greeting"] == "Добрый день"
