import json
import logging
from datetime import datetime

import pandas as pd

from src.utils import get_currency_rates, get_greeting, get_stock_prices, load_transactions

logger = logging.getLogger(__name__)


def home_page(date_str: str) -> str:
    """
    Возвращает JSON-ответ для страницы «Главная».

    Args:
        date_str (str): Дата в формате 'YYYY-MM-DD HH:MM:SS'

    Returns:
        str: JSON-строка с данными
    """
    # Парсинг даты
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        target_date = dt.date()
    except ValueError as e:
        logger.error(f"Некорректный формат даты: {e}")
        return json.dumps({"error": "Некорректный формат даты"}, ensure_ascii=False, indent=2)

    # Загрузка транзакций
    try:
        df = load_transactions("data/operations.xlsx")
    except Exception as e:
        logger.error(f"Ошибка загрузки транзакций: {e}")
        df = pd.DataFrame()

    # Фильтрация по дате (с начала месяца до target_date)
    if not df.empty:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"])
        mask = (df["Дата операции"].dt.date >= target_date.replace(day=1)) & \
               (df["Дата операции"].dt.date <= target_date)
        filtered_df = df[mask]
    else:
        filtered_df = pd.DataFrame()

    # Приветствие
    greeting = get_greeting(dt.hour)

    # Данные по картам
    cards_data = []
    if not filtered_df.empty:
        for last_digits in filtered_df["Номер карты"].unique():
            card_transactions = filtered_df[filtered_df["Номер карты"] == last_digits]
            total_spent = card_transactions["Сумма операции"].sum()
            cashback = total_spent / 100
            cards_data.append({
                "last_digits": str(last_digits),
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2)
            })

    # Топ-5 транзакций по сумме платежа
    top_transactions = []
    if not filtered_df.empty:
        top_transactions = filtered_df.nlargest(5, "Сумма платежа")[[
            "Дата операции", "Сумма платежа", "Категория", "Описание"
        ]].to_dict(orient="records")
        for item in top_transactions:
            item["date"] = item["Дата операции"].strftime("%d.%m.%Y")
            item["amount"] = item["Сумма платежа"]
            item["category"] = item["Категория"]
            item["description"] = item["Описание"]
            del item["Дата операции"], item["Сумма платежа"], item["Категория"], item["Описание"]

    # Курсы валют и цены акций (единая обработка настроек)
    currency_rates = []
    stock_prices = []

    try:
        with open("user_settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка чтения user_settings.json: {e}")
        settings = {"user_currencies": [], "user_stocks": []}

    # Курсы валют
    if "user_currencies" in settings and settings["user_currencies"]:
        try:
            currency_rates = get_currency_rates(settings["user_currencies"])
        except Exception as e:
            logger.error(f"Ошибка получения курсов валют: {e}")
    else:
        logger.warning("user_currencies не найден или пуст в настройках")

    # Цены акций
    if "user_stocks" in settings and settings["user_stocks"]:
        try:
            stock_prices = get_stock_prices(settings["user_stocks"])
        except Exception as e:
            logger.error(f"Ошибка получения цен акций: {e}")
    else:
        logger.warning("user_stocks не найден или пуст в настройках")

    # Формирование JSON
    result = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(result, ensure_ascii=False, indent=2)
