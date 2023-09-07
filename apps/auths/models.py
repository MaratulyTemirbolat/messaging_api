# Python
from typing import (
    Any,
    Optional,
)

# Django
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    BooleanField,
    BigIntegerField,
    QuerySet,
)

# Project
from abstracts.models import AbstractDateTime


class CustomUserManager(BaseUserManager):
    """CustomUserManger."""

    def __obtain_user_instance(
        self,
        login: str,
        first_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        """Get user instance."""
        if not first_name.strip():
            raise ValidationError(
                message="First name is required.",
                code="firt_name_empty"
            )

        new_user: 'CustomUser' = self.model(
            login=login,
            first_name=first_name,
            password=password,
            **kwargs
        )
        return new_user

    def create_user(
        self,
        login: str,
        first_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        """Create Custom user."""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            login=login,
            first_name=first_name,
            password=password,
            **kwargs
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
        self,
        login: str,
        first_name: str,
        password: str,
        **kwargs: dict[str, Any]  # kwargs -> key word arguments
    ) -> 'CustomUser':
        """Create super user."""
        new_user: 'CustomUser' = self.__obtain_user_instance(
            login=login,
            first_name=first_name,
            password=password,
            **kwargs
        )
        new_user.is_staff = True
        new_user.is_superuser = True
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def get_deleted(self) -> QuerySet:
        """Get deleted users."""
        return self.filter(
            datetime_deleted__isnull=False
        )

    def get_not_deleted(self) -> QuerySet:
        """Get not deleted users."""
        return self.filter(
            datetime_deleted__isnull=True
        )

    def get_user_by_login(self, login: str) -> Optional['CustomUser']:
        """Get user by provided login."""
        user: Optional['CustomUser'] = None
        try:
            user = self.get(login=login)
            return user
        except CustomUser.DoesNotExist:
            return None


class CustomUser(
    AbstractBaseUser,
    PermissionsMixin,
    AbstractDateTime
):
    """CustomUser model database."""
    LOGIN_MAX_LEN = 200
    FIRST_NAME_LEN = 254

    login: CharField = CharField(
        max_length=LOGIN_MAX_LEN,
        unique=True,
        db_index=True,
        verbose_name="Логин"
    )
    telegram_id: BigIntegerField = BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Идентификатор чата"
    )
    first_name: CharField = CharField(
        max_length=FIRST_NAME_LEN,
        verbose_name="Имя"
    )
    is_active: BooleanField = BooleanField(
        default=True,
        verbose_name="Активность",
        help_text="True - ваш акк активный, False - удален"
    )
    is_staff: BooleanField = BooleanField(
        default=False,
        verbose_name="Статус менеджера"
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS: list[str] = [
        "first_name",
        "password",
    ]

    class Meta:
        """Customization of the Model (table)."""

        ordering: tuple[str] = (
            "-datetime_updated",
        )
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"

    def __str__(self) -> str:
        return self.login

    def recover(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        """Recover the user if he is deleted."""
        if self.datetime_deleted:
            self.datetime_deleted = None
            self.save(
                update_fields=['datetime_deleted']
            )

    def set_telegram_id(self, telegram_id: int) -> None:
        """Set telegram state in CustomUser if it isn't."""
        if not self.telegram_id:
            self.telegram_id = telegram_id
            self.save(
                update_fields=['telegram_id']
            )
