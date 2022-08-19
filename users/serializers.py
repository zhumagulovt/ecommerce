from django.core import exceptions
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework import exceptions as drf_exceptions
from rest_framework.settings import api_settings

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSerializer
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'password_confirm'
        ]
    
    def validate(self, data):
        # remove from data, because it's not User model's field
        password_confirm = data.pop('password_confirm', None)
 
        user = User(**data)
        password = data.get('password')

        # password validation
        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        # password confirm validation
        if password != password_confirm:
            raise serializers.ValidationError({"Пароли не совпадают"})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password')
        )

        return user


class UserChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        user = self.context.get('user')
        
        if not user.check_password(current_password):
            raise serializers.ValidationError(
                {"current_password": "Текущий пароль введен неправильно"}
            )
        
        if current_password == new_password:
            raise serializers.ValidationError(
                {"new_password": "Новый пароль похож на старый"}
            )
        
        # password validation
        try:
            validate_password(new_password, user)
        except exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"new_password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    
  
    # Overiding validate function in the TokenObtainSerializer  
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        try:
            user = User.objects.get(email=authenticate_kwargs['email'])
            if not user.is_active:
                self.error_messages['no_active_account']=(
                    'Этот аккаунт не активен'
                )
                raise drf_exceptions.AuthenticationFailed(
                    self.error_messages['no_active_account'],
                    'no_active_account',
                )

        except User.DoesNotExist:
            self.error_messages['no_active_account'] =(
                'Почта не зарегистрирована')
            raise drf_exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            self.error_messages['no_active_account'] = (
                'Неверный пароль')
            raise drf_exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        return super().validate(attrs)
