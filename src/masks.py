from typing import List
import logging


logger = logging.getLogger('masks')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/masks.log')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(number_card: List[str]) -> str:
    """Функция, которая принимает номер карты в виде числа и возвращает
     маску"""
    if len(number_card) < 16:
        logger.warning("Неправильно введен номер карты")
        return ""
    number_card_1 = "".join(number_card)
    number_card_1 = number_card_1.replace(" ", "")
    mask_card = " ".join(number_card_1[i : i + 4] for i in range(0, len(number_card_1), 4))
    mask_card_list = list(mask_card)

    for i in range(len(mask_card_list)):
        if 7 <= i <= 13 and mask_card_list[i] != " ":
            mask_card_list[i] = "*"
    mask_card_number = "".join(mask_card_list)
    logger.info("Успешно создана маска карты")
    return mask_card_number


def get_mask_account(number_cart):
    """Функция, которая принимает номер счета в виде числа и
    возвращает маску"""
    if len(number_cart) < 20:
        logger.warning("Неправильно введен номер счета")
        return ""
    number_cart = number_cart.replace(" ", "")
    number_mask = str(number_cart[-4:])
    logger.info("Успешно создана маска счета")
    return f"**{number_mask}"
