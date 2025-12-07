import logging
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла."""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Загружено {len(df)} транзакций из {file_path}")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки файла {file_path}: {e}")
        raise


def get_greeting(hour: int) -> str:
    """Возвращает приветствие по времени суток."""
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:  # 23–5
        return "Доброй ночи"


def get_currency_rates(currencies):
    try:
        response = requests.get("ВАШ_API_URL")
        data = response.json()
        rates = []
        for currency in currencies:
            if currency in data["rates"] and data["rates"][currency] > 0:
                rates.append({
                    "currency": currency,
                    "rate": data["rates"][currency]
                })
        return rates
    except (KeyError, ConnectionError, ValueError):
        return []


def get_stock_prices(stocks):
    prices = []
    for stock in stocks:
        try:
            response = requests.get(f"...{stock}")
            data = response.json()
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                prices.append({
                    "stock": stock,
                    "price": float(data["Global Quote"]["05. price"])
                })
        except (KeyError, ValueError, TypeError):
            continue  # пропускаем акции без данных
    return prices
