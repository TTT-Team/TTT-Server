from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import BankAccount, Currency


class Transaction(models.Model):
    METHOD_CHOICES = [
        ('SBP', 'СБП'),
        ('On_account', 'На банковский счет')
    ]

    bank_account_from = models.ForeignKey(
        BankAccount,
        verbose_name="Счет снятия средств",
        null=False,
        on_delete=models.CASCADE,
        related_name="bank_account_from"
    )
    bank_account_to = models.ForeignKey(
        BankAccount,
        verbose_name="Счет пополнения средств",
        null=False,
        on_delete=models.CASCADE,
        related_name="bank_account_to"
    )
    summ = models.IntegerField(
        verbose_name="Количество средств",
        validators=[MinValueValidator(-20000), MaxValueValidator(20000)],
        unique=False,
        null=False
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name="Валюта",
        null=False,
        on_delete=models.CASCADE
    )
    method = models.CharField(
        verbose_name="Способ перевода",
        choices=METHOD_CHOICES,
        unique=False,
        null=False,
        default='SBP',
    )
    date_created = models.DateTimeField(verbose_name='Дата проведения операции', auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'



