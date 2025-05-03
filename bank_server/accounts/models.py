import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from accounts.utils import create_bank_account_number
from bank_server import settings


def validate_username(value):
    if not re.match(r"^[a-zA-Zа-яА-Я]+$", value):
        raise ValidationError("Имя пользователя может содержать только латинские и кириллические символы.")

def validate_phone(value):
    if not re.match(r"^[0-9]{10}$", value):
        raise ValidationError("Телефон должен содержать только цифры и быть в длину 10 символов")

def validate_account(value):
    if not re.match(r"^[0-9]{20}$", value):
        raise ValidationError("Номер счета должен содержать только цифры и быть в длину 20 символов")


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True, blank=False, null=False)
    first_name = models.CharField(
        max_length=50,
        unique=False,
        null=False,
        validators=[validate_username],
        verbose_name="Имя"
    )
    second_name = models.CharField(
        max_length=80,
        unique=False,
        null=False,
        validators=[validate_username],
        verbose_name="Фамилия"
    )
    phone = models.CharField(
        max_length=10,
        unique=True,
        null=False,
        validators=[validate_phone],
        verbose_name="Телефон"
    )

    class Meta:
        db_table = 'auth_user'  # Стандартное имя таблицы для совместимости

    def save(self, *args, **kwargs):
        created = not self.pk  # Проверяем, новый ли пользователь
        super().save(*args, **kwargs)  # Сначала сохраняем пользователя

        if created:
            # Генерация номера счета
            account_number = create_bank_account_number(self.pk, "Debit", "RUB")

            BankAccount.objects.create(
                user=self,
                account_number=account_number,
                type='Debit',
                currency='RUB',
                balance=0
            )


class BankAccount(models.Model):
    TYPE_CHOICES = [
        ('Debit', 'Дебетовый'),
        ('Credit', 'Кредитный'),
        ('Contribution', 'Вклад')
    ]

    CURRENCY_CHOICES = [
        ('RUB', 'Российский Рубль'),
        ('USD', 'Американский Доллар'),
        ('CNY', 'Китайский Юань'),
        ('AMD', 'Армянский драм'),
        ('GEL', 'Грузинский лари'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        null=False,
        on_delete=models.CASCADE
    )
    account_number = models.CharField(
        verbose_name="Номер счета",
        max_length=20,
        unique=True,
        null=False,
        validators=[validate_account],
    )
    type = models.CharField(
        verbose_name="Тип счета",
        max_length=12,
        choices=TYPE_CHOICES,
        unique=False,
        null=False,
        default='Debit',
    )
    currency = models.CharField(
        verbose_name="Валюта",
        max_length=3,
        choices=CURRENCY_CHOICES,
        unique=False,
        null=False,
        default='RUB',
    )
    balance = models.IntegerField(
        verbose_name="Количество средств",
        unique=False,
        null=False,
        default=0,
    )
    time_create = models.DateTimeField(verbose_name='Дата создания счета', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Дата изменения счета', auto_now=True)


    def __str__(self):
        return f"{self.user} - {self.type}"

    class Meta:
        db_table = 'bank_accounts'
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'
