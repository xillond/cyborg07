from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, first_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    first_name = models.CharField(
        max_length=123,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=123,
        verbose_name='Фамилия',
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Номер телефона'
    )
    avatar = models.ImageField(
        upload_to='user_avatar',
        default='user_avatar/defaultpfp.jpg',
        verbose_name='Аватарка',
        blank=True,
        null=True
    )
    role = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Модератор'),
            (3, 'Бухгалтер'),
        ),
        default=1,
        verbose_name='Роль'
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    is_admin = models.BooleanField(
        default=False
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    def __str__(self):
        return f"{self.first_name}"

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'