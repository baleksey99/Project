import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
url = "https://api.apilayer.com/exchangerates_data/convert"


def convert_transaction_to_rub(transaction: dict) -> float:
    """
    Функция принимает на вход транзакцию и возвращает сумму в рублях.
    """
    currency = transaction.get("operationAmount").get("currency").get("code")
    amount_cur = float(transaction.get("operationAmount").get("amount"))

    if currency == "RUB":
        return amount_cur
    else:
        payload = {
            "amount": amount_cur,
            "from": currency,
            "to": "RUB"
        }
        headers = {
            "apikey": API_KEY
        }

        response = requests.get(url, headers=headers, params=payload)

        if response.status_code == 200:
            result = response.json()
            return round(float(result.get("result")), 2)
        else:
            raise Exception("Ошибка при обращении к API")