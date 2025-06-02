from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """обрабатывает информацию о картах и счетах и выводит замаскированный номер"""
    parts = info.split()
    type_info = " ".join(parts[:-1])
    number = parts[-1]

    if "счет" in type_info.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(list(number))

    return f"{type_info} {masked_number}"


print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))


def get_date(info: str) -> str:
    """Функция, которая возвращает строку с датой в формате "ДД.ММ.ГГГГ" """
    date = f"{info[8:10]}.{info[5:7]}.{info[0:4]}"
    return date


print(get_date("2024-03-11T02:26:18.671407"))
