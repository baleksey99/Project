"""
Единый модуль для запуска всей функциональности проекта.
"""
import argparse
import sys
from datetime import datetime

# Импортируем функционал из модулей проекта
from src.reports import spending_by_category
from src.services import investment_bank
from src.utils import get_currency_rates, get_greeting, get_stock_prices
from src.views import home_page  # предположим, есть такая функция


def cmd_greeting():
    """Вывести приветствие по текущему часу."""
    hour = datetime.now().hour
    print(get_greeting(hour))


def cmd_spending_by_category(category: str, date_str: str):
    """Показать траты по категории за дату."""
    # Здесь нужно подставить реальный DataFrame, например, из load_transactions
    # Для примера просто вызываем функцию
    result = spending_by_category(None, category, date_str)
    print(result)


def cmd_investment_bank(month: int, limit: float):
    """Рассчитать инвестиционный доход."""
    result = investment_bank(month, [], limit)  # [] — пример пустых транзакций
    print(f"Доход: {result}")


def cmd_currency_rates(currencies: list):
    """Получить курсы валют."""
    rates = get_currency_rates(currencies)
    for item in rates:
        print(f"{item['currency']}: {item['rate']}")


def cmd_stock_prices(symbols: list):
    """Получить цены акций."""
    prices = get_stock_prices(symbols)
    for item in prices:
        print(f"{item['stock']}: {item['price']}")


def cmd_homepage():
    """Отрисовать главную страницу (если есть веб‑часть)."""
    html = home_page()
    print(html)


def main():
    parser = argparse.ArgumentParser(description="Универсальный запускатель проекта")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Подкоманды
    subparsers.add_parser("greeting", help="Вывести приветствие")

    spend_parser = subparsers.add_parser("spending", help="Траты по категории")
    spend_parser.add_argument("category", type=str, help="Название категории")
    spend_parser.add_argument("date", type=str, help="Дата в формате ГГГГ-ММ-ДД")

    invest_parser = subparsers.add_parser("investment", help="Инвестиционный расчёт")
    invest_parser.add_argument("month", type=int, help="Номер месяца")
    invest_parser.add_argument("limit", type=float, help="Лимит")

    rates_parser = subparsers.add_parser("rates", help="Курсы валют")
    rates_parser.add_argument("currencies", nargs="+", help="Список валют (USD EUR и т. п.)")

    stocks_parser = subparsers.add_parser("stocks", help="Цены акций")
    stocks_parser.add_argument("symbols", nargs="+", help="Тикеры акций (AAPL GOOG и т. п.)")

    subparsers.add_parser("homepage", help="Отрисовать главную страницу")

    args = parser.parse_args()

    if args.command == "greeting":
        cmd_greeting()
    elif args.command == "spending":
        cmd_spending_by_category(args.category, args.date)
    elif args.command == "investment":
        cmd_investment_bank(args.month, args.limit)
    elif args.command == "rates":
        cmd_currency_rates(args.currencies)
    elif args.command == "stocks":
        cmd_stock_prices(args.symbols)
    elif args.command == "homepage":
        cmd_homepage()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
