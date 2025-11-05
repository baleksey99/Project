import csv
import pandas as pd


def reading_transactions_csv(file_path: str) -> list:
    """ Считывает финансовые операции из CSV-файла и возвращает список словарей с транзакциями """
    try:
        transactions_csv = []
        with open(file_path, 'r', newline='', encoding='utf-8') as csv_f:
            rd_transactions_csv = csv.DictReader(csv_f, delimiter=';')
            for row in rd_transactions_csv:
                transactions_csv.append(row)
        return transactions_csv
    except FileNotFoundError:
        return []


def read_from_excel(file_path) -> list[dict]:
    """Функция принимает пусть к файлу формата excel и возвращает список словарей."""
    try:
        excel_data = pd.read_excel(file_path).to_dict(orient="records")
        return excel_data
    except FileNotFoundError:
        return []
