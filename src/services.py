import math
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
        month: строка формата 'ГГГГ-ММ' (например, '2025-03')
        transactions: список транзакций со полями:
            - 'Дата операции': строка в формате 'ГГГГ-ММ-ДД'
            - 'Сумма операции': число или строка (будет преобразовано в float)
        limit: целое число — шаг округления


    Returns:
        Сумма накоплений после округления (округлена до 2 знаков после запятой)
    """
    try:
        # Разбираем месяц и год из строки
        target_year, target_month = map(int, month.split('-'))
        total_saved = 0.0

        print(f"\n=== Начало расчёта для месяца {month}, лимит={limit} ===")

        for transaction in transactions:
            # Преобразуем дату операции
            tx_date = datetime.strptime(transaction['Дата операции'], '%Y-%m-%d')

            # Проверяем, относится ли транзакция к целевому месяцу
            if tx_date.year == target_year and tx_date.month == target_month:
                amount = float(transaction['Сумма операции'])

                # Отладка: выводим обрабатываемую сумму и лимит
                print(f"Обработка транзакции: сумма={amount}, лимит={limit}")

                # Проверяем, кратно ли amount лимиту
                quotient = amount / limit
                if quotient != math.floor(quotient):
                    # Округляем вверх до ближайшего кратного limit
                    rounded = (math.floor(quotient) + 1) * limit
                    saved = rounded - amount
                    total_saved += saved
                    print(f"  → Округлено до {rounded}, сэкономлено: {saved}")
                else:
                    print("  → Сумма уже кратна лимиту, экономия: 0.0")

        # Округляем итоговую сумму до 2 знаков после запятой
        result = round(total_saved, 2)
        print(f"=== Итого накоплено: {result} ===")
        return result

    except (ValueError, KeyError, TypeError, AttributeError) as e:
        print(f"Ошибка при обработке данных: {e}")
        return 0.0
