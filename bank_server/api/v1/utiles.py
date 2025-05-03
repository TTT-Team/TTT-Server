from rest_framework.exceptions import ParseError

from accounts.models import BankAccount


def check_credit_debt(user, bank_account):
    if bank_account.type == 'Debit':
        bank_accounts_credit = BankAccount.objects.filter(type='Credit', user=user)

        if bank_accounts_credit:
            for acc in bank_accounts_credit:
                if acc.balance <= -20000:
                    raise ParseError(f"Есть непокрытый кредит в {acc.balance}")
