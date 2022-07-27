from django.db import models
import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin

 
class MyUserManager(BaseUserManager):
    def _create_user(self, email, first_name, password, **extra_fields):
        if not email: 
            raise ValueError("Вы не ввели Email")
        if not first_name:
            raise ValueError("Вы не ввели Имя")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, password):
        return self._create_user(email, first_name, password)

    def create_superuser(self, email, first_name, password):
        return self._create_user(email, first_name, password, is_staff=True, is_superuser=True)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True) # Идентификатор
    email = models.EmailField(max_length=100, unique=True) # Email
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Имя') # Имя
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Фамилия') # Фамилия
    is_active = models.BooleanField(default=True) # Статус активации
    is_staff = models.BooleanField(default=False) # Статус админа
    
    USERNAME_FIELD = 'email' # Идентификатор для обращения
    REQUIRED_FIELDS = ['first_name']
 
    objects = MyUserManager() # Добавляем методы класса MyUserManager
    # Метод для отображения в админ панели

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

class Company(models.Model):
	name = models.CharField(max_length=255)
	users = models.ManyToManyField(User)

	def __str__(self):
		return self.name