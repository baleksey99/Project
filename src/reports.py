import logging
from datetime import datetime
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)


def spending_by_category(
        df: pd.DataFrame,
        category: str,
        start_date: str
) -> Dict[str, Any]:

    """
    Формирует отчёт «Траты по категории» за трёхмесячный период.


    Args:
        df (pd.DataFrame): DataFrame с транзакциями (обязательные столбцы:
            'Дата операции', 'Категория', 'Сумма операции')
        category (str): Название категории для анализа
        start_date (str): Дата начала периода в формате 'YYYY-MM-DD'


    Returns:
        Dict[str, Any]: Словарь с данными отчёта:
            - 'category': искомая категория
            - 'period': строка с диапазоном дат
            - 'total_spent': общая сумма трат
            - 'transactions_count': количество транзакций
            - 'average_transaction': средняя сумма транзакции
            - 'monthly_breakdown': детализация по месяцам

    """
    try:
        # Парсинг даты начала
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = (start + pd.DateOffset(months=3)) - pd.Timedelta(days=1)
        end_date = end.date()

        # Фильтрация по категории и периоду
        df['Дата операции'] = pd.to_datetime(df['Дата операции']).dt.date
        mask = (
            (df['Категория'] == category)
            & (df['Дата операции'] >= start)
            & (df['Дата операции'] <= end_date)
        )
        filtered = df[mask].copy()

        if filtered.empty:
            logger.warning(f"Нет транзакций по категории '{category}' за период {start} – {end_date}")
            return {
                "category": category,
                "period": f"{start} – {end_date}",
                "total_spent": 0.0,
                "transactions_count": 0,
                "average_transaction": 0.0,
                "monthly_breakdown": []
            }

        # Расчёты
        total_spent = filtered['Сумма операции'].sum()
        transactions_count = len(filtered)
        average_transaction = total_spent / transactions_count

        # Детализация по месяцам
        filtered['Месяц'] = filtered['Дата операции'].apply(
            lambda d: d.strftime('%Y-%m')
        )
        monthly = filtered.groupby('Месяц').agg({
            'Сумма операции': 'sum',
            'Дата операции': 'count'
        }).reset_index()
        monthly_breakdown = [
            {
                "month": row['Месяц'],
                "total": round(row['Сумма операции'], 2),
                "count": row['Дата операции']
            }
            for _, row in monthly.iterrows()
        ]

        return {
            "category": category,
            "period": f"{start} – {end_date}",
            "total_spent": round(total_spent, 2),
            "transactions_count": transactions_count,
            "average_transaction": round(average_transaction, 2),
            "monthly_breakdown": monthly_breakdown
        }

    except (ValueError, KeyError, TypeError) as e:
        logger.error(f"Ошибка в spending_by_category: {e}")
        raise
