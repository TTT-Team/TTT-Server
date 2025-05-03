from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

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
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )

        return user