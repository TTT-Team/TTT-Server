from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError

from accounts.models import BankAccount


def check_credit_debt(user, bank_account):
    """Проверяет наличие большой задолжности по кредиту"""
    if bank_account.type == 'Debit':
        bank_accounts_credit = BankAccount.objects.filter(type='Credit', user=user)

        if bank_accounts_credit:
            for acc in bank_accounts_credit:
                if acc.balance <= -20000:
                    raise ParseError(f"Есть непокрытый кредит в {acc.balance}")



def check_valid_data_request(user, data_amount, data_bank_account):
    """Проверяет валидность переданных данных"""
    if not data_amount:
        raise ParseError("Не указана сумма!")

    if data_amount <= 0:
        raise ParseError("Сумма должна быть положительной")

    if not data_bank_account:
        raise ParseError("Не указан счет!")

    bank_account_current = get_object_or_404(BankAccount, account_number=data_bank_account, user=user)
    bank_account_currency = bank_account_current.currency

    check_credit_debt(user, bank_account_current)

    return bank_account_current, bank_account_currency