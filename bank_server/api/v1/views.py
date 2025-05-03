from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import LoginSerializer, RegisterSerializer


@extend_schema(
    tags=["auth"],
    summary="Авторизация пользователя",
    description="Аутентификация по номеру телефона и паролю.",
    examples=[
        OpenApiExample(
            "Пример запроса",
            value={"phone": "9123456789", "password": "mypassword"},
            request_only=True
        ),
        OpenApiExample(
            "Пример ответа",
            value={
                "message": "Успешный вход",
                "user": {
                    "id": 1,
                    "phone": "9123456789",
                    "first_name": "Иван"
                },
                "csrf_token": "abc123..."
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

        if not user:
            return Response(
                {"detail": "Неверный номер телефона или пароль"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Создаем сессию
        login(request, user)
        # Получаем CSRF-токен (для защиты форм)
        csrf_token = get_token(request)

        response_data = {
            "message": "Успешный вход",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "csrf_token": csrf_token
        }

        return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["auth"],
    summary="Выход из системы",
    description="""
    Завершает текущую сессию пользователя. Требует:
    - Действующей сессии (куки sessionid)
    - CSRF-токена в заголовке X-CSRFToken
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
    responses={
        200: OpenApiResponse(
            description='Успешный выход',
            examples=[
                OpenApiExample(
                    "Пример ответа",
                    value={"message": "Успешный выход"},
                    response_only=True
                )
            ]
        ),
        403: OpenApiResponse(
            description='Ошибка CSRF или аутентификации',
            examples=[
                OpenApiExample(
                    "Ошибка CSRF",
                    value={"detail": "CSRF Failed: CSRF token missing or incorrect"},
                    response_only=True
                ),
                OpenApiExample(
                    "Не авторизован",
                    value={"detail": "Authentication credentials were not provided."},
                    response_only=True
                )
            ]
        )
    },
    examples=[
        OpenApiExample(
            "Пример запроса",
            value={},  # Тело запроса пустое для logout
            request_only=True,
            media_type='application/json'
        )
    ]
)
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Успешный выход"}, status=status.HTTP_200_OK)

@extend_schema(
    tags=["auth"],
    summary="Регистрация нового пользователя",
    description='Создает нового пользователя и автоматически открывает дебетовый счет в RUB',
    examples=[
        OpenApiExample(
            'Пример запроса',
            value={
                "username": "ivanov",
                "email": "ivan@example.com",
                "first_name": "Иван",
                "last_name": "Иванов",
                "phone": "9123456789",
                "password": "securePassword123",
                "password_confirm": "securePassword123"
            },
            request_only=True
        )
    ]
)
class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Создаем сессию
        login(request, user)
        # Получаем CSRF-токен (для защиты форм)
        csrf_token = get_token(request)

        response_data = {
            "message": "Пользователь успешно зарегистрирован",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            "csrf_token": csrf_token
        }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )