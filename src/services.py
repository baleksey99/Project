from datetime import datetime
from typing import Any, Dict, List


def investment_bank(
        month: str,
        transactions: List[Dict[str, Any]],
        limit: int
) -> float:
    """
    Рассчитывает сумму, отложенную в «Инвесткопилку» за указанный месяц
    путём округления транзакций до заданного лимита.

    Args:
        month (str): Месяц в формате 'YYYY-MM' (например, '2025-03')
        transactions (List[Dict[str, Any]]): Список транзакций со полями:
            - 'Дата операции' (str): дата в формате 'YYYY-MM-DD'
            - 'Сумма операции' (float): сумма транзакции
        limit (int): Лимит округления (10, 50 или 100)


    Returns:
        float: Сумма, отложенная в «Инвесткопилку» (округлена до 2 знаков)


    Example:
        >>> transactions = [
        ...     {'Дата операции': '2025-03-15', 'Сумма операции': 1712.0},
        ...     {'Дата операции': '2025-03-20', 'Сумма операции': 847.5}
        ... ]
        >>> investment_bank('2025-03', transactions, 50)
        50.5  # 38 (от 1712) + 12.5 (от 847.5)
    """
    try:
        # Парсинг месяца
        target_year, target_month = map(int, month.split('-'))

        total_saved = 0.0

        for transaction in transactions:
            # Парсинг даты транзакции
            tx_date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')

            # Проверка, относится ли транзакция к целевому месяцу
            if tx_date.year == target_year and tx_date.month == target_month:
                amount = float(transaction['Сумма операции'])

                # Округление вверх до ближайшего кратного limit
                if amount % limit != 0:
                    rounded = ((amount // limit) + 1) * limit
                    saved = rounded - amount
                    total_saved += saved

        return round(total_saved, 2)

    except (ValueError, KeyError, TypeError) as e:
        import logging
        logging.error(f"Ошибка в investment_bank: {e}")
        return 0.0
