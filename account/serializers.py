from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class UserRegistrSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['email', 'first_name', 'password']
 

	def validate(self, data):
		user = User(**data)
		password = data.get('password')

		errors = dict() 
		try:
			validators.validate_password(password=password, user=User)
		except exceptions.ValidationError as e:
			errors['password'] = list(e.messages)

		if errors:
			raise serializers.ValidationError(errors)

		return super(UserRegistrSerializer, self).validate(data)

	def save(self, *args, **kwargs):
		user = User(
			email=self.validated_data['email'], # Назначаем Email
			first_name=self.validated_data['first_name'], # Назначаем Логин
		)
		password = self.validated_data['password']
		user.set_password(password)
		user.save()
		token = Token.objects.create(user=user)
		return {'token': 'Token '+token.key}

class LoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=255)
	first_name = serializers.CharField(max_length=255, read_only=True)
	password = serializers.CharField(max_length=128, write_only=True)

	def validate(self, data):
		email = data.get('email', None)
		password = data.get('password', None)

		if email is None:
			raise serializers.ValidationError(
				'Для входа требуется адрес электронной почты.'
			)
		if password is None:
			raise serializers.ValidationError(
				'Для входа требуется пароль.'
			)
		user = authenticate(email=email, password=password)
		if user is None:
			raise serializers.ValidationError(
				'Пользователь с таким адресом электронной почты и паролем не найден.'
			)
		if not user.is_active:
			raise serializers.ValidationError(
				'Этот пользователь деактивирован.'
			)
		token = Token.objects.get(user=user)
		return {'token': 'Token '+token.key}