import os
import src.utils
from src.utils import filter_transactions_by_currency
from src.reader import reading_transactions_csv

json_path = os.path.join(os.getcwd(), "data", "operations.json")
csv_path = os.path.join(os.getcwd(), "data", "transactions.csv")
xlsx_path = os.path.join(os.getcwd(), "data", "transactions_excel.xlsx")

def main():

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

# Выбор формата файла
    file_format = input()

    if file_format == "1":
        print("Для обработки выбран JSON-файл.")
        transactions = filter_transactions_by_currency(json_path)
        print(transactions)

    elif file_format == "2":
        print("Для обработки выбран CSV-файл.")
        transaction = reading_transactions_csv(csv_path)

    elif file_format == "3":
        print("Для обработки выбран XLSX-файл.")

    else:
        print("Программа: Неверный формат файла. Завершение работы.")
        return


if __name__ == "__main__":
    main()