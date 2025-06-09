from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinValueValidator
from pytils.translit import slugify
from rest_framework import serializers

from accounts.models import validate_account, validate_phone, BankAccount

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(
        max_length=10,
        required=True,
        help_text="Номер телефона пользователя"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Пароль пользователя"
    )

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not phone or not password:
            raise serializers.ValidationError("Необходимо указать телефон и пароль")

        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone',
            'password',
            'password_confirm'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True}
        }

    def validate(self, attrs):
        # Проверка совпадения паролей
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        # Дополнительная валидация телефона
        phone = attrs.get('phone')
        if phone and User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "Этот телефон уже зарегистрирован"})

        return attrs

    def create(self, validated_data):
        # Удаляем подтверждение пароля перед созданием пользователя
        validated_data.pop('password_confirm')

        # Создаем пользователя с хешированием пароля
        user = User.objects.create_user(
            username=f"{slugify(validated_data['first_name'])}_{slugify(validated_data['last_name'])}",
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )

        return user


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,  # Общее количество цифр
        decimal_places=2,
        required=True,
        validators=[MinValueValidator(0.01)]
    )
    bank_account = serializers.CharField(
        max_length=20,
        required=True,
        validators=[validate_account],
    )

    def validate(self, attrs):
        amount = attrs.get('amount')
        bank_account = attrs.get('bank_account')

        if not amount or not bank_account:
            raise serializers.ValidationError("Необходимо указать сумму и номер счета")

        return attrs


class TransferSBPSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,  # Общее количество цифр
        decimal_places=2,
        required=True,
        validators=[MinValueValidator(0.01)]
    )
    bank_account = serializers.CharField(
        max_length=20,
        required=True,
        validators=[validate_account],
    )
    to_client_phone = serializers.CharField(
        max_length=10,
        required=True,
        validators=[validate_phone],
    )

    def validate(self, attrs):
        amount = attrs.get('amount')
        bank_account = attrs.get('bank_account')
        to_client_phone = attrs.get('to_client_phone')

        if not amount or not bank_account or not to_client_phone:
            raise serializers.ValidationError("Необходимо указать сумму, номер счета и телефон получателя")

        return attrs


class TransferAccountSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,  # Общее количество цифр
        decimal_places=2,
        required=True,
        validators=[MinValueValidator(0.01)]
    )
    bank_account = serializers.CharField(
        max_length=20,
        required=True,
        validators=[validate_account],
    )
    to_client_bank_account_number = serializers.CharField(
        max_length=20,
        required=True,
        validators=[validate_account],
    )

    def validate(self, attrs):
        amount = attrs.get('amount')
        bank_account = attrs.get('bank_account')
        to_client_bank_account_number = attrs.get('to_client_bank_account_number')

        if not amount or not bank_account or not to_client_bank_account_number:
            raise serializers.ValidationError("Необходимо указать сумму, номера счетов отправителя и получателя")

        return attrs


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            'id', 'account_number', 'type',
            'currency', 'balance', 'isMain',
            'time_create', 'time_update'
        ]
        read_only_fields = [
            'id', 'account_number',
            'time_create', 'time_update'
        ]

    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("Баланс не может быть отрицательным")
        return value
