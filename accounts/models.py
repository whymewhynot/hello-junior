from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    city = models.ForeignKey('jobs.City', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город')
    skills = models.ManyToManyField('jobs.Skill', null=True, blank=True, verbose_name='Навыки')
    is_subscribed = models.BooleanField(default=True, verbose_name='Подписка на рассылку')
    registered = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    remote = models.BooleanField(default=False, null=True, blank=True, verbose_name='Удалённая работа')

    favorites = models.ManyToManyField('jobs.Job', null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'auth_user'

