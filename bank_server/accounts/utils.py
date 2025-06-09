def create_bank_account_number(id_client: int, type_account: str, currency: str) -> str:
    """Генерирует номер счета клиента
    :param id_client: ID клиента
    :param type_account: Тип счета
    :param currency: Валюта

    :return Сгенерированный номер счета
    """

    balance_1 = '423' if type_account == 'Contribution' else '408'  # Тип счёта

    # Уточнение категории счёта (4-5 цифры)
    balance_2 = '17'  # 17 - рублёвый счёт для резидентов (физлиц)
    if type_account == 'Contribution':
        balance_2 = '00'

    # Код валюты (6-8 цифры)
    kod_currency = '810'  # По умолчанию RUB
    match currency:
        case 'USD':
            kod_currency = '840'
        case 'EUR':
            kod_currency = '978'
        case 'CNY':
            kod_currency = '156'
        case 'AMD':
            kod_currency = '051'
        case 'GEL':
            kod_currency = '981'
        case _:
            kod_currency = '810'  # RUB по умолчанию

    kontrol_number = '9'  # Контрольная цифра
    kod_filial_bank = '0001'  # Код филиала банка
    number_ls = str(id_client).zfill(7)  # Уникальный номер клиента внутри банка

    return f'{balance_1}{balance_2}{kod_currency}{kontrol_number}{kod_filial_bank}{number_ls}'
