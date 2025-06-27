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


def get_date(info: str) -> str:
    """Функция, которая возвращает строку с датой в формате "ДД.ММ.ГГГГ" или пустую строку, если даты нет"""
    if len(info) < 10 or not info[0:4].isdigit() or not info[5:7].isdigit() or not info[8:10].isdigit():
        return ""  # Возвращаем пустую строку, если дата отсутствует
    date = f"{info[8:10]}.{info[5:7]}.{info[0:4]}"
    return date
