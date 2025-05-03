from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter, OpenApiRequest
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import BankAccount
from api.v1 import utiles
from api.v1.serializers import LoginSerializer, RegisterSerializer


@extend_schema(
    tags=["auth"],
    summary="Авторизация пользователя",
    description="Аутентификация по номеру телефона и паролю.",
    request=OpenApiExample('Запрос'),
    responses={
        200: OpenApiExample('Успешная авторизация')
    },
    examples=[
        OpenApiExample(
            "Запрос",
            value={"phone": "9123456789", "password": "mypassword"},
            request_only=True
        ),
        OpenApiExample(
            "Успешная авторизация",
            value={
                "message": "Успешный вход",
                "user": {
                    "id": 1,
                    "phone": "9123456789",
                    "first_name": "Иван"
                },
                "JWT-token": "abc123...",
                "Refresh-token": "dadasd...."
            },
            response_only=True
        )
    ]
)
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        # Аутентификация пользователя
        user = authenticate(request, phone=phone, password=password)
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        if not user:
            return Response(
                {"detail": "Неверный номер телефона или пароль"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response_data = {
            "message": "Успешный вход",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "JWT-token": access_token,
            "Refresh-token": str(refresh_token)
        }

        return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["auth"],
    summary="Выход из системы (JWT)",
    description="""
        Деактивирует refresh-токен пользователя.
        Требует валидного refresh-токена в теле запроса.
        """,
    parameters=[
        OpenApiParameter(
            name='X-CSRFToken',
            description='CSRF-токен (получить через /auth/get-csrf/)',
            required=True,
            type=str,
            location=OpenApiParameter.HEADER
        )
    ],
    request=OpenApiExample("Запрос"),
    responses={
        200: OpenApiExample("Успешный выход"),
        400: OpenApiExample("Ошибка Refresh-token"),
        403: OpenApiExample("Пример запроса"),
    },
    examples=[
        OpenApiExample(
            "Запрос",
            value={"refresh": "ваш_refresh_токен"},
            request_only=True,
            media_type='application/json'
        ),
        OpenApiExample(
            "Успешный выход",
            value={"message": "Успешный выход"},
            status_codes=['200'],
            response_only=True
        ),
        OpenApiExample(
            "Ошибка Refresh-token",
            value={"detail": "Неверный refresh токен"},
            status_codes=['400'],
            response_only=True
        ),
        OpenApiExample(
            "Не авторизован",
            value={"detail": "Authentication credentials were not provided."},
            status_codes=['403'],
            response_only=True
        )

    ]
)
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавляем токен в черный список
            return Response(
                {"message": "Успешный выход"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Неверный refresh токен"},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["auth"],
    summary="Регистрация нового пользователя",
    description='Создает нового пользователя и автоматически открывает дебетовый счет в RUB',
    request=OpenApiExample("Пример запроса"),
    responses={
        200: OpenApiExample('Успешная регистрация')
    },
    examples=[
        OpenApiExample(
            'Пример запроса',
            value={
                "email": "ivan@example.com",
                "first_name": "Иван",
                "last_name": "Иванов",
                "phone": "9123456789",
                "password": "securePassword123",
                "password_confirm": "securePassword123"
            },
            request_only=True
        ),
        OpenApiExample(
            'Успешная регистрация',
            value={
                "message": "Пользователь успешно зарегистрирован",
                "user": {
                    "id": '1',
                    "phone": '79123456789',
                    "first_name": 'Иван',
                    "last_name": 'Иванов',
                    "email": "ivan@example.com",
                },
                "JWT-token": "abc123...",
                "Refresh-token": "dadasd...."
            }
        )
    ]
)
class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        response_data = {
            "message": "Пользователь успешно зарегистрирован",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "JWT-token": access_token,
            "Refresh-token": str(refresh_token)
        }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["bank_account"],
    summary="Пополнение счета",
    description="""
    API для пополнения дебетового счета пользователя. 
    Требуется предоставление суммы пополнения и номера счета.
    Ограничения:
    - Для счетов в валюте сумма пополнения (в пересчете на рубли) не должна превышать 30,000 рублей.
    - Для рублевых счетов сумма пополнения также не должна превышать 30,000 рублей.
    - Если сумма превышает 1,000,000 рублей, к счету добавляется бонус в размере 2,000 рублей.
    """,
    request=OpenApiExample("Запрос"),
    responses={
        200: OpenApiExample("Успешное пополнение"),
        400: OpenApiExample("Ошибочный запрос"),
        404: OpenApiExample("Счет не найден")
    },
    examples=[
        OpenApiExample(
            'Запрос',
            value={
                "amount": 15000,
                "bank_account": "4100123456789"
            },
            request_only=True
        ),
        OpenApiExample(
            "Успешное пополнение",
            value={
                "message": "Счет успешно пополнен",
                "bank_account_number": "4100123456789",
                "new_balance": 1015000
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            "Ошибка: превышен лимит суммы",
            value={"detail": "Сумма превышает порог в 30000 рублей"},
            response_only=True,
            status_codes=["400"]
        ),
        OpenApiExample(
            "Ошибочный запрос",
            value={"detail": "Не указана сумма пополнения!"},
            response_only=True,
            status_codes=["400"]
        ),
        OpenApiExample(
            "Счет не найден",
            value={"detail": "Указанный счет не найден"},
            response_only=True,
            status_codes=["404"]
        ),
    ]
)
class DepositAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data_amount = request.data.get('amount', None)
        data_bank_account = request.data.get('bank_account', None)

        if not data_amount:
            raise ParseError("Не указана сумма пополнения!")

        if data_amount <= 0:
            raise ParseError("Сумма пополнения должна быть положительной")

        if not data_bank_account:
            raise ParseError("Не указан счет!")

        bank_account_debit = get_object_or_404(BankAccount, account_number=data_bank_account, user=user)
        bank_account_currency = bank_account_debit.currency

        utiles.check_credit_debt(user, bank_account_debit)

        if bank_account_currency.kod != 'RUB':
            if bank_account_currency.course * data_amount > 30000:
                raise ParseError("Сумма превышает порог в 30000 рублей")
        else:
            if data_amount > 30000:
                raise ParseError("Сумма превышает порог в 30000 рублей")

        if data_amount > 1000000:
            bank_account_debit.balance = bank_account_debit.balance + data_amount + 2000
        else:
            bank_account_debit.balance = bank_account_debit.balance + data_amount

        bank_account_debit.save()

        return Response(
            {
                "message": "Счет успешно пополнен",
                "bank_account_number": bank_account_debit.account_number,
                "new_balance": bank_account_debit.balance
            },
            status=status.HTTP_200_OK
        )
