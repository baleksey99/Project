import json
from datetime import datetime

import pandas as pd

from src.utils import get_currency_rates, get_stock_prices, load_transactions


def home_page(current_time_str: str) -> str:
    """
    Возвращает JSON-строку с данными для главной страницы:
    - приветствие
    - карты и траты по ним
    - курсы валют
    - цены акций

    Args:
        current_time_str: строка с датой и временем в формате 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'

    Returns:
        JSON-строка с данными
    """
    # Парсим текущее время
    current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S')

    # Загружаем транзакции (с обработкой ошибок)
    try:
        transactions = load_transactions()
    except Exception as e:
        print(f"Ошибка загрузки транзакций: {e}")
        transactions = pd.DataFrame(columns=[
            "Дата операции", "Номер карты", "Сумма операции", "Категория", "Описание"
        ])

    # Загружаем курсы валют и цены акций
    try:
        currency_rates = get_currency_rates()
    except Exception as e:
        print(f"Ошибка загрузки курсов валют: {e}")
        currency_rates = []

    try:
        stock_prices = get_stock_prices()
    except Exception as e:
        print(f"Ошибка загрузки цен акций: {e}")
        stock_prices = []

    # Формируем приветствие
    hour = current_time.hour
    if 5 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 17:
        greeting = "Добрый день"
    elif 17 <= hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    # Агрегируем траты по картам
    cards = []
    if not transactions.empty:
        # Группируем по номеру карты и считаем общую сумму трат
        card_groups = transactions.groupby("Номер карты")
        for card_number, group in card_groups:
            total_spent = group["Сумма операции"].sum()
            # Берём последние 4 цифры номера карты
            last_digits = str(card_number)[-4:]
            cards.append({
                "last_digits": last_digits,
                "total_spent": round(total_spent, 2)
            })

    # Формируем итоговый ответ
    result = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": transactions.head(5).to_dict('records'),  # Топ-5 транзакций
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(result, ensure_ascii=False, indent=2)
