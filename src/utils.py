
import logging
import os

from typing import Dict, List

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
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    elif 17 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """Получает курсы валют через API."""
    api_key = open(".env").read().split("EXCHANGE_API_KEY=")[1].strip()
    try:
        response = requests.get(
            "https://api.exchangerate-api.com/v4/latest/RUB",
            params={"access_key": api_key}
        )
        data = response.json()
        rates = data["rates"]
        return [
            {"currency": curr, "rate": round(rates.get(curr, 0.0), 2)}
            for curr in currencies
        ]
    except Exception as e:
        logger.error(f"Ошибка получения курсов валют: {e}")
        return [{"currency": curr, "rate": 0.0} for curr in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    try:
        api_key = os.getenv("STOCK_API_KEY")
        if not api_key:
            raise ValueError("Ключ STOCK_API_KEY не найден в .env")

        prices = []
        for symbol in stocks:
            response = requests.get(
                "https://www.alphavantage.co/query",
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": api_key
                }
            )
            response.raise_for_status()

            data = response.json().get("Global Quote", {})
            if not data:
                logger.error(f"API вернул пустой ответ для {symbol}")
                price = 0.0
            else:
                # Преобразуем строку в float
                price_str = data.get("05. price", "0.0")
                try:
                    price = float(price_str)
                except ValueError:
                    logger.error(f"Не удалось преобразовать цену для {symbol}: {price_str}")
                    price = 0.0

            prices.append({"stock": symbol, "price": round(price, 2)})

        return prices
    except Exception as e:
        logger.error(f"Ошибка получения цен акций: {e}")
        return [{"stock": symbol, "price": 0.0} for symbol in stocks]
