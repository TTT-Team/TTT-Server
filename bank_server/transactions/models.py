from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import BankAccount, Currency


class Transaction(models.Model):
    METHOD_CHOICES = [
        ('SBP', 'Перевод по СБП'),
        ('Account', 'Перевод на банковский счет'),
        ('Withdraw', 'Снятие средств'),
        ('Deposit', 'Пополнение средств')
    ]

    bank_account_from = models.ForeignKey(
        BankAccount,
        verbose_name="Счет снятия средств",
        null=True,
        on_delete=models.CASCADE,
        related_name="bank_account_from",
        blank=False,
    )
    bank_account_to = models.ForeignKey(
        BankAccount,
        verbose_name="Счет пополнения средств",
        null=True,
        on_delete=models.CASCADE,
        related_name="bank_account_to",
        blank=False,
    )
    amount = models.DecimalField(
        verbose_name="Количество средств",
        decimal_places=2,
        max_digits=12,
        unique=False,
        null=False,
        blank=True,
        default=0.0,
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name="Валюта",
        null=False,
        on_delete=models.CASCADE,
        blank=True,
    )
    method = models.CharField(
        verbose_name="Тип транзакции",
        choices=METHOD_CHOICES,
        unique=False,
        null=False,
        default='SBP',
        blank=True,
    )
    date_created = models.DateTimeField(verbose_name='Дата проведения операции', auto_now_add=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'



