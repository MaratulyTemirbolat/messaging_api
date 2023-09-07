# Rest Framework
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    DateTimeField,
    Serializer,
    CharField,
)

# Project
from auths.models import CustomUser
from abstracts.serializers import AbstractDateTimeSerializer


class CustomUserListSerializer(AbstractDateTimeSerializer, ModelSerializer):
    """CustomUserListSerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted

    class Meta:
        """Customization of the serializer."""

        model: CustomUser = CustomUser
        fields: tuple[str] = (
            "id",
            "login",
            "first_name",
            "is_active",
            "is_staff",
            "datetime_created",
            "is_deleted",
        )


class CustomUserCreateSerializer(ModelSerializer):
    """CustomUserCreateSerializer."""

    class Meta:
        """Customization of the Serializer."""

        model: CustomUser = CustomUser
        fields: tuple[str] = (
            "login",
            "first_name",
            "password",
        )


class CustomUserForeignKeySerializer(
    AbstractDateTimeSerializer,
    ModelSerializer
):
    """CustomUserForeignKeySerializer."""

    datetime_created: DateTimeField = \
        AbstractDateTimeSerializer.datetime_created
    is_deleted: SerializerMethodField = \
        AbstractDateTimeSerializer.is_deleted

    class Meta:
        """Customization of the serializer."""

        model: CustomUser = CustomUser
        fields: tuple[str] = (
            "id",
            "login",
            "first_name",
            "is_active",
            "is_staff",
            "datetime_created",
            "is_deleted",
        )


class CustomUserLoginSerializer(Serializer):
    """CustomUserLoginSerializer."""

    login: CharField = CharField()
    password: CharField = CharField()
