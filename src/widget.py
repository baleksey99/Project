from typing import List
from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(info: str) -> str:
    """обрабатывает информацию о картах и счетах и выводит замаскированный номер"""
    parts = info.split()
    type_info = " ".join(parts[:-1])
    number = parts[-1]

    if 'счет' in type_info.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(list(number))

    return f"{type_info} {masked_number}"

print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))



